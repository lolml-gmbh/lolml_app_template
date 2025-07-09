# Copyright (c) 2024 [LOLML GmbH](https://lolml.com/), Julian Wergieluk, George Whelan
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field

from dotenv import load_dotenv

DEFAULT_CMP_OP = ">="

if os.path.exists(".env.shared"):
    load_dotenv(".env.shared")
load_dotenv(".env")
PACKAGE_MANAGER = os.getenv("PACKAGE_MANAGER", "conda")
DEFAULT_ENV_NAME = os.getenv("ENV_NAME", "lolbot")


@dataclass
class PackageSpec:
    name: str
    version: str
    cmp_op: str
    install_from_url: str = field(default="")


def get_package_name_from_url(url: str) -> str:
    # Ex: 'git+ssh://git@github.com/lolml-gmbh/portfolio_tracker.git@main'
    package_name = url.split("/")[-1]
    if "@" in url:
        package_name = package_name.split("@")[0]
    if package_name.endswith(".git"):
        package_name = package_name[:-4]
    return package_name


def read_package_specs(file_path: str) -> list[PackageSpec]:
    with open(file_path) as file:
        package_list = file.read().splitlines()

    package_data = []
    for i, package_line in enumerate(package_list):
        package_line = package_line.strip()
        if package_line.startswith("#"):
            continue
        if not package_line:
            continue
        cmp_op = ""
        version = ""
        if package_line.startswith("git+ssh") or package_line.startswith("git+http"):
            package_name = get_package_name_from_url(package_line)
            package_data.append(
                PackageSpec(
                    name=package_name, version=version, cmp_op=cmp_op, install_from_url=package_line
                )
            )
            continue
        if "#" in package_line:
            package_line = package_line.split("#")[0].strip()
        if "<" in package_line and "<=" not in package_line:
            raise ValueError(f"Package line {i}: {package_line}: operator `<` is not supported")
        if ">" in package_line and ">=" not in package_line:
            raise ValueError(f"Package line {i}: {package_line}: operator `>` is not supported")
        if "<=" in package_line:
            cmp_op = "<="
        if ">=" in package_line:
            cmp_op = ">="
        if "==" in package_line:
            cmp_op = "=="
        if cmp_op:
            package_name, version = package_line.split(cmp_op)
        else:
            package_name = package_line

        package_data.append(PackageSpec(name=package_name, version=version, cmp_op=cmp_op))
    return package_data


def write_package_specs(file_path: str, package_specs: list[PackageSpec]):
    spec_lines = []
    for package_spec in package_specs:
        if package_spec.cmp_op and not package_spec.install_from_url:
            spec_lines.append(f"{package_spec.name}{package_spec.cmp_op}{package_spec.version}")
        elif package_spec.install_from_url:
            spec_lines.append(f"{package_spec.install_from_url}")
        else:
            spec_lines.append(f"{package_spec.name}")

    # spec_lines.sort()
    spec = "\n".join(spec_lines) + "\n"
    with open(file_path, "w") as f:
        f.write(spec)


def get_env_package_versions(env_name: str) -> dict[str, str]:
    command = f"{PACKAGE_MANAGER} list -n {env_name} --json".split(" ")
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout
    output_data = json.loads(output)

    env_package_versions = {}
    for p in output_data:
        env_package_versions[p["name"]] = p["version"]

    command = "pip list --format=json".split(" ")
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    output = result.stdout
    output_data = json.loads(output)
    for p in output_data:
        if p["name"] in env_package_versions:
            continue
        env_package_versions[p["name"]] = p["version"]
    return env_package_versions


def remove_non_digit_chars(version: str) -> str:
    return "".join([c for c in version if c.isdigit()])


def version_less_op(version0: str, version1: str) -> bool:
    # Evaluate x0.y0.z0 < x1.y1.z1
    v0 = [remove_non_digit_chars(v) for v in version0.split(".")]
    v1 = [remove_non_digit_chars(v) for v in version1.split(".")]
    num_version_parts = min(len(v0), len(v1))
    num_version_parts = min(num_version_parts, 3)
    for i in range(num_version_parts):
        if int(v0[i]) < int(v1[i]):
            return True
        if int(v0[i]) > int(v1[i]):
            return False
    return False  # Add this line to handle cases where versions are equal


def update_package_versions_from_env(
    package_specs: list[PackageSpec], env_name: str, ignore_missing: bool = False
) -> list[PackageSpec]:
    env_package_versions = get_env_package_versions(env_name)
    package_specs_dict = {p.name: p for p in package_specs}
    updated_package_specs = []
    for name, spec in package_specs_dict.items():
        if name in env_package_versions:
            env_version = env_package_versions[name]
            if spec.version and version_less_op(env_version, spec.version):
                raise ValueError(
                    f"Environment {env_name} has version {env_version} of package {name}, but "
                    f"{spec.version} is required"
                )
            cmp_op = spec.cmp_op if spec.cmp_op else DEFAULT_CMP_OP
            updated_spec = PackageSpec(name=name, version=env_version, cmp_op=cmp_op, install_from_url=spec.install_from_url)
            updated_package_specs.append(updated_spec)
        elif not ignore_missing:
            raise ValueError(f"Package '{name}' not found in the environment '{env_name}'")
        else:
            updated_package_specs.append(spec)
    return updated_package_specs


def update_requirements(env_name: str, path: str, ignore_missing: bool = False) -> None:
    requirements = read_package_specs(path)
    updated_requirements = update_package_versions_from_env(requirements, env_name, ignore_missing)
    write_package_specs(path, updated_requirements)


def check_requirements(env_name: str, path: str) -> None:
    # check if the environment has the required packages
    requirements = read_package_specs(path)
    env_package_versions = get_env_package_versions(env_name)
    for package in requirements:
        if package.name not in env_package_versions:
            raise ValueError(f"Package '{package.name}' not found in the environment '{env_name}'")


def check_package_manager(package_manager: str) -> bool:
    if shutil.which(package_manager):
        result = subprocess.run([package_manager, "--version"], capture_output=True)
        return result.returncode == 0
    return False


def main(args: list[str]) -> int:
    if not check_package_manager(PACKAGE_MANAGER):
        print(f"Package manager '{PACKAGE_MANAGER}' not found in PATH")
        return 1

    if not args:
        print("Usage: python requirements_checker.py [update|check] [env_name]")
        return 0
    env = args[1] if len(args) > 1 else DEFAULT_ENV_NAME
    if not env:
        print("No environment name provided")
        return 1

    try:
        if args[0] in ("update", "u"):
            update_requirements(env, "requirements_conda.txt")
            update_requirements(env, "requirements_pip.txt", True)
            return 0
        if args[0] in ("check", "c"):
            check_requirements(env, "requirements_conda.txt")
            check_requirements(env, "requirements_pip.txt")
            return 0
    except ValueError as e:
        print(f"REQUIREMENTS CHECKER ERROR: {e}")
        raise


if __name__ == "__main__":
    return_code = main(sys.argv[1:])
    sys.exit(return_code)

# Copyright (c) 2025 LOLML GmbH (https://lolml.com/)
import streamlit as st

APP_TITLE = "LOLML App Template"
LEGAL_NOTICE = """
### Legal Notice

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
COPYRIGHT_LINE = """
App made by: LOLML GmbH](https://lolml.com/)

Like what you see? :sparkles: Let's have a :coffee: and talk about your next ML project.
"""
COL_FAV = "fav"
st.set_page_config(page_title=APP_TITLE, page_icon=":rocket:", layout="wide")


def main() -> None:
    st.title(APP_TITLE)
    st.logo("lolml.png", link="https://lolml.com/")

    st.markdown(COPYRIGHT_LINE)
    st.caption(LEGAL_NOTICE)


if __name__ == "__main__":
    main()

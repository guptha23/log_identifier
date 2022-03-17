import streamlit as st
import re
import textwrap

# wrapping text by breaking it to multiple lines so that it's easy to read 
def print_large_text(text):
    """ wraps and prints text based on charecter limit for each row. """
    text = str(text)
    text = text.replace("\n\t", " ")
    text = text.replace("\n\tat", " at")
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text_wrapper = textwrap.TextWrapper(width=100)
    wrapped_text_list = text_wrapper.wrap(text)
    return "\n".join(wrapped_text_list)

st.title("Log Helper - Find things easily with logs...")

uploaded_files = st.file_uploader("Choose one or more log files", accept_multiple_files=True)

concatenate_all_files = st.checkbox("Concatenate all the attached files")

bytes_data = ""

if concatenate_all_files:
    st.write("Combining the following files..")

    for uploaded_file in uploaded_files:
        st.write("filename: ", uploaded_file.name)
        bytes_data += str(uploaded_file.read())

else:
    selectbox = st.selectbox(
    "Select a single required log file ",
    [file_.name for file_ in uploaded_files])

    st.write(f"You selected {selectbox}")

    for uploaded_file in uploaded_files:
        if selectbox == uploaded_file.name:
            bytes_data += str(uploaded_file.read())



keyword = st.text_input("Enter the sentence or phrase to be searched for : ", "ArrayOutOfBoundsException")
st.write("We are trying to search for ", keyword)

list_of_matches = []

if keyword is not None:

    list_of_matches = [m.start() for m in re.finditer(keyword, bytes_data)]
    st.metric("Number of matches found : ", len(list_of_matches))

    choice = st.number_input("Pick the required match ", 1, len(list_of_matches)+1)

    if len(list_of_matches) > 0 and choice < len(list_of_matches):
        
        number = choice - 1
        count = int(2000)
        char_index = int(list_of_matches[number])
        st.write(f"Getting the {choice} match :")

        text = bytes_data[char_index : char_index + count].replace("\n\t", " ")

        st.code("> " + print_large_text(text), language="shell")

        print_more_info = st.checkbox("log more information")

        if print_more_info:
            count += 4000
            text = bytes_data[char_index : char_index + count].replace("\n\t", " ")

            st.code("> " + print_large_text(text), language="shell")

    else:
        st.write("No suitable match found")

        


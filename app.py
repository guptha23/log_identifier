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
    text_wrapper = textwrap.TextWrapper(width=75)
    wrapped_text_list = text_wrapper.wrap(text)
    return "\n".join(wrapped_text_list)


def process_key_matches(bytes_data, list_of_matches):
    """ helper function to process list of matches found. """

    st.metric("Number of matches found : ", len(list_of_matches))

    choice = st.number_input("Pick the required match ", 1, len(list_of_matches))

    if len(list_of_matches) > 0 and choice < len(list_of_matches):
        
        number = choice - 1
        count = int(2000)

        char_index = int(list_of_matches[number])

        st.write(f"Getting the {choice} match :")

        print_prev_info = st.checkbox("log previous information")

        if print_prev_info:
            text = bytes_data[char_index - 500 : char_index].replace("\n\t", " ")

            st.code("> " + print_large_text(text), language="shell")

        text = bytes_data[char_index : char_index + count].replace("\n\t", " ")

        st.code("> " + print_large_text(text), language="shell")

        print_next_info = st.checkbox("log next information")


        if print_next_info:
            text = bytes_data[char_index + count : char_index + count + 500].replace("\n\t", " ")

            st.code("> " + print_large_text(text), language="shell")



    else:
        st.write("No suitable match found")


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


    if "|" in keyword:
        keywords = keyword.split("|")
        keywords = [word.strip() for word in keywords]

        list_of_matches = []

        for keyword in keywords:
            list_of_matches += [m.start() for m in re.finditer(keyword, bytes_data,  re.IGNORECASE)]

        process_key_matches(bytes_data, list_of_matches)

    # elif "&" in keyword:
    #     keywords = keyword.split("&")
    #     keywords = [word.strip() for word in keywords]

    #     list_of_matches_dict = {}

    #     for keyword in keywords:
    #         list_of_matches_dict[keyword] = [m.start() for m in re.finditer(keyword, bytes_data, re.IGNORECASE)]

    #     print(list_of_matches_dict)

    #     list_of_lists = list(list_of_matches_dict.values())
    #     list_of_matches = list(set.intersection(*map(set,list_of_lists)))
    #     print("list of matches : ",list_of_matches)

    #     process_key_matches(bytes_data, list_of_matches)

    else:

        list_of_matches = [m.start() for m in re.finditer(keyword, bytes_data, re.IGNORECASE)]
        process_key_matches(bytes_data, list_of_matches)
            


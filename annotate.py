import streamlit as st
import PyPDF2
from docxlatex import Document
from PIL import Image
import fitz
import io
import os
import json
import pandas as pd

# Định nghĩa hàm để đọc nội dung từ tệp DOCX
def read_docx(file):
    doc = Document(file)
    docx = doc.get_text()
    return docx

# Định nghĩa hàm để đọc nội dung từ tệp PDF
def read_pdf(file):
    pdf_file = fitz.open(file)
    for page_number in range(len(pdf_file)): 
        page=pdf_file[page_number]
        image_list = page.get_images()
        print(image_list)
        
        for image_index, img in enumerate(page.get_images(),start=1):
            print(image_index)
            xref = img[0] 
            # extract image bytes 
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            # get image extension
            image_ext = base_image["ext"]
            
    # Create a PIL Image object from the image bytes
            pil_image = Image.open(io.BytesIO(image_bytes))

            # Save the image to disk
            image_path = f"image_{page_number}_{image_index}.{image_ext}"
            pil_image.save(image_path)
    

# Tiêu đề của ứng dụng
st.title('HiHi')
folder_path = r'C:\UIT\MMMU\csv'

csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

current_index = st.session_state.get("current_index", 0)

# lấy ra file trong thư mục 
csv_file_path = os.path.join(folder_path, csv_files[current_index])

st.write(f"Đang thực hiện trên file {csv_files[current_index]}")
df = pd.read_csv(csv_file_path)

# hiển thị từng câu hỏi trong file
df_index= st.session_state.get("df_index", 0)
item = (df.iloc[df_index, :])

question = st.text_input('Câu hỏi', value= item['question'])
choices = st.text_area('Các lựa chọn', value= item['choices'])
answer = st.text_input('Đáp án đúng', value= '')
explain = st.text_input('Giải thích', value= '')
subject = st.text_input('Môn học', value= item['subject'])
grade = st.text_input('Lớp', value=item['grade'])
image_file_name = []
uploaded_images = st.file_uploader("Kéo hoặc tải lên ảnh", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Thư mục để lưu trữ ảnh
output_dir = "uploaded_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if uploaded_images is not None:
    for i, uploaded_image in enumerate(uploaded_images):
        filename = f"uploaded_image_{i+1}.jpg"
        image_file_name.append(filename)
        # Đường dẫn đến file ảnh
        filepath = os.path.join(output_dir, filename)
        # Lưu ảnh vào thư mục đích
        with open(filepath, "wb") as f:
            f.write(uploaded_image.getbuffer())

if st.button("SUBMIT"):
    new_data = {
        'question': question,
        'choices': choices,
        'answer': answer,
        'explain': explain,
        'images': image_file_name,
        'subject': subject,
        'grade': grade
    }
    print(new_data)

if st.button("Next question") and df_index < len(df)-1:
    df_index += 1
    st.session_state["df_index"] = df_index
    st.rerun()

if st.button("Next file") and current_index < len(csv_files) - 1:
    st.session_state["df_index"] = 0 # khởi tạo lại vị trí bắt đầu của từng câu hỏi
    current_index += 1
    st.session_state["current_index"] = current_index
    st.rerun()
else:
    st.write("Không còn file JSON nào trong thư mục.")


# folder_path = r"C:\UIT\MMMU\JSON and IMAGES of PDF\Json"
# json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

# current_index = st.session_state.get("current_index", 0)
# if json_files:
#     current_file = json_files[current_index]
#     st.write(f"Đang thực hiện trên file {current_file}")

#     # Đọc nội dung của file JSON
#     file_path = os.path.join(folder_path, current_file)
#     with open(file_path, "r", encoding="utf-8") as f:
#         json_data = f.read()
#     json_list = json_data.strip().split('\n')
#     for json_str in json_list:
#         st.write(json_str['question'])
#     # Nút Next để chuyển qua file tiếp theo
#     if st.button("Next") and current_index < len(json_files) - 1:
#             current_index += 1
#             st.session_state["current_index"] = current_index
#     else:
#         st.write("Không có file JSON nào trong thư mục.")

# initial_question = 'cau hoi'
# initial_choices = 'cac lua chon'
# initial_answer = 'dap an'
# initial_explain = 'giai thich'
# st.markdown("# Câu 1")
# question = st.text_input('Câu hỏi', value= initial_question)
# choices = st.text_input('Các lựa chọn', value= initial_choices)
# answer = st.text_input('Đáp án đúng', value= initial_answer)
# explain = st.text_input('Giải thích', value= initial_explain)
# subject = st.text_input('Môn học')
# grade = st.text_input('Lớp')

# data = {
#               'question': question,
#               'choices': choices,
#               'answer': answer,
#               'explain': explain
#         }
#           # Thêm các ảnh vào data
# # for idx, image in enumerate(images, start=1):
# #     data[f'image_{idx}'] = image
# #     data['subject'] = subject
# #     data['grade'] = grade

# if st.button("Submit"):
#     print(question)
#     print(choices)
#     print(answer)
#     print(explain)

# # Tải lên tệp
# uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'])

# # Hiển thị nội dung tệp
# if uploaded_file is not None:
#     if uploaded_file.type == 'application/msword' or uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
#         st.write(read_docx(uploaded_file))
#     st.write(uploaded_file)

# from streamlit_pdf_viewer import pdf_viewer
# pdf_viewer(r"C:\UIT\MMMU\Files\thuvienhoclieu.com-De-on-thi-HK1-Toan-12-nam-22-23-De4 - officeMath.docx")
import tkinter as tk
from tkinter import scrolledtext, ttk
import re


def modify_css():
    # 입력 텍스트 가져오기
    css_input = input_text.get("1.0", tk.END)

    # 사용자 입력 가져오기
    class_names = class_entry.get().strip()
    property_name = property_entry.get().strip()
    new_value = new_value_entry.get().strip()

    # 입력 유효성 검사
    if not class_names or not property_name or not new_value:
        status_label.config(text="클래스, 속성, 새 값을 모두 입력해주세요.", fg="red")
        return

    # 클래스 이름 분리 (쉼표, 공백으로 구분)
    class_list = [c.strip() for c in re.split(r'[,\s]+', class_names) if c.strip()]

    # 각 클래스 이름에 점(.)이 없으면 추가
    class_list = ['.' + c if not c.startswith('.') else c for c in class_list]

    modified_css = css_input
    modified_classes = []
    not_found_classes = []

    # 각 클래스에 대해 속성 수정
    for class_name in class_list:
        # 클래스가 있는지 확인
        if class_name in modified_css:
            # 정규식 패턴 생성
            pattern = r"({}[^{{]*?{{[^}}]*?)({}\s*:\s*[^;]+)([^}}]*?}})".format(
                re.escape(class_name),
                re.escape(property_name)
            )

            # 속성이 있는지 확인하기 위한 패턴
            check_pattern = r"{}[^{{]*?{{[^}}]*?{}\s*:".format(
                re.escape(class_name),
                re.escape(property_name)
            )

            if re.search(check_pattern, modified_css):
                # 속성이 있으면 수정
                new_css = re.sub(pattern, r"\1{}:{}\3".format(property_name, new_value), modified_css)
                if new_css != modified_css:
                    modified_css = new_css
                    modified_classes.append(class_name)
            else:
                # 속성이 없으면 추가
                pattern = r"({}[^{{]*?{{)([^}}]*?}})".format(re.escape(class_name))
                new_css = re.sub(pattern, r"\1\n    {}: {};\2".format(property_name, new_value), modified_css)
                if new_css != modified_css:
                    modified_css = new_css
                    modified_classes.append(class_name)
        else:
            not_found_classes.append(class_name)

    # 결과 출력
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", modified_css)

    # 상태 메시지 생성
    if modified_classes:
        status_message = f"다음 클래스의 CSS가 수정되었습니다: {', '.join(modified_classes)}"
        status_color = "green"
    else:
        status_message = "수정된 클래스가 없습니다."
        status_color = "orange"

    if not_found_classes:
        status_message += f"\n다음 클래스를 찾을 수 없습니다: {', '.join(not_found_classes)}"
        status_color = "orange"

    status_label.config(text=status_message, fg=status_color)


# 메인 윈도우 생성
root = tk.Tk()
root.title("CSS 스타일 수정기")
root.geometry("800x700")

# 프레임 생성
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

# 입력 필드 프레임
input_fields_frame = tk.LabelFrame(frame, text="수정 옵션", padx=10, pady=10)
input_fields_frame.pack(fill=tk.X, pady=(0, 10))

# 입력 필드 그리드 배치
tk.Label(input_fields_frame, text="클래스 이름(들):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
class_entry = ttk.Entry(input_fields_frame, width=40)
class_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
class_entry.insert(0, "e40_253, e40_252")  # 기본값 - 여러 클래스 예시

tk.Label(input_fields_frame, text="속성 이름:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
property_entry = ttk.Entry(input_fields_frame, width=20)
property_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
property_entry.insert(0, "width")  # 기본값

tk.Label(input_fields_frame, text="새 값:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
new_value_entry = ttk.Entry(input_fields_frame, width=20)
new_value_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
new_value_entry.insert(0, "220px")  # 기본값

# 클래스 입력 도움말
help_label = tk.Label(input_fields_frame, text="여러 클래스는 쉼표(,)나 공백으로 구분하세요", fg="gray", font=("Arial", 8))
help_label.grid(row=0, column=2, sticky="w", padx=5, pady=5)

# 열 가중치 설정
input_fields_frame.columnconfigure(1, weight=1)

# 입력 영역 레이블
input_label = tk.Label(frame, text="CSS 코드 입력:")
input_label.pack(anchor="w", pady=(0, 5))

# 입력 텍스트 영역
input_text = scrolledtext.ScrolledText(frame, height=10, width=80, wrap=tk.WORD)
input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

# 변환 버튼
convert_button = tk.Button(frame, text="CSS 수정하기", command=modify_css, bg="#4CAF50", fg="white", padx=10, pady=5)
convert_button.pack(pady=10)

# 상태 레이블
status_label = tk.Label(frame, text="", font=("Arial", 10), justify=tk.LEFT)
status_label.pack(pady=(0, 10), anchor="w")

# 출력 영역 레이블
output_label = tk.Label(frame, text="수정된 CSS 코드:")
output_label.pack(anchor="w", pady=(0, 5))

# 출력 텍스트 영역
output_text = scrolledtext.ScrolledText(frame, height=10, width=80, wrap=tk.WORD)
output_text.pack(fill=tk.BOTH, expand=True)

# 샘플 CSS 코드 미리 입력
sample_css = """.e40_252 { 
    background-color:#E5E0E0;
    width:291px;
    height:980px;
    position:absolute;
    left:1111px;
    top:0px;
}
.e40_253 { 
    color:#000000;
    width:73px;
    height:385px;
    position:absolute;
    left:51px;
    top:146px;
    font-family:Inter;
    text-align:center;
    font-size:64px;
    letter-spacing:0;
}"""

input_text.insert("1.0", sample_css)

# 메인 루프
root.mainloop()

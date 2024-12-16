import os
import zipfile
import time
import shutil

def monitor_and_zip(source_folder, destination_folder, threshold=32, file_types=('.webp', '.png', '.jpeg')):
    """
    특정 폴더 및 하위 폴더를 모니터링하고, 지정된 파일 형식의 파일 개수가 threshold를 넘으면 파일들을 zip으로 압축하여 다른 폴더로 이동합니다.

    Args:
        source_folder: 모니터링할 폴더의 경로.
        destination_folder: 압축된 zip 파일을 저장할 폴더 경로.
        threshold: 파일 개수 임계값.
        file_types: 카운트할 파일 형식들의 튜플 (예: ('.webp', '.png', '.jpeg'))
    """

    while True:
        count = 0
        for root, _, files in os.walk(source_folder): # 하위 폴더까지 탐색
            for file in files:
                if file.lower().endswith(file_types): # 확장자 비교 (대소문자 구분 없이)
                    count += 1

        if count > threshold:
            source_folder_name = os.path.basename(source_folder)
            zip_filename = f"{source_folder_name}_{time.strftime('%Y%m%d%H%M%S')}.zip"
            zip_filepath = os.path.join(destination_folder, zip_filename)

            with zipfile.ZipFile(zip_filepath, 'w') as zipf:
                for root, _, files in os.walk(source_folder): # 하위 폴더까지 탐색
                    for file in files:
                        if file.lower().endswith(file_types):
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, arcname=os.path.relpath(file_path, source_folder)) # 상대 경로 사용

            # 원본 파일 삭제 (필요에 따라 주석 해제)
            for root, _, files in os.walk(source_folder):
                for file in files:
                    if file.lower().endswith(file_types):
                        os.remove(os.path.join(root, file))
            print(f"압축 파일 {zip_filepath} 생성 및 원본 파일 삭제 완료.")

        time.sleep(10)


# 사용 예시:
source_folder = "/content/Fooocus/outputs"  # 모니터링할 폴더 경로를 지정합니다.
destination_folder = "/content/drive/MyDrive/Loras/outputs"  # 압축 파일 저장할 폴더 경로를 지정합니다.

# 폴더가 존재하지 않으면 생성합니다.
#os.makedirs(source_folder, exist_ok=True)
#os.makedirs(destination_folder, exist_ok=True)


monitor_and_zip(source_folder, destination_folder)

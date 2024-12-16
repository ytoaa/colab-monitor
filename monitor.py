import os
import zipfile
import time
import shutil

def monitor_and_zip(source_folder, destination_folder, threshold=32):
    """
    특정 폴더를 모니터링하고, 파일 개수가 threshold를 넘으면 파일들을 zip으로 압축하여 다른 폴더로 이동합니다.

    Args:
        source_folder: 모니터링할 폴더의 경로.
        destination_folder: 압축된 zip 파일을 저장할 폴더 경로.
        threshold: 파일 개수 임계값.
    """

    while True:  # 무한 루프로 모니터링
        files = os.listdir(source_folder)
        num_files = len(files)

        if num_files > threshold:
            zip_filename = f"{source_folder.split('/')[-1]}_{time.strftime('%Y%m%d%H%M%S')}.zip"  # 파일 이름 생성
            zip_filepath = os.path.join(destination_folder, zip_filename)

            with zipfile.ZipFile(zip_filepath, 'w') as zipf:
                for file in files:
                    file_path = os.path.join(source_folder, file)
                    zipf.write(file_path, arcname=file)  # arcname을 사용하여 압축 파일 내에서의 파일 이름을 유지

            # 원본 파일 삭제 (필요에 따라 주석 해제)
            for file in files:
                os.remove(os.path.join(source_folder, file))  
            print(f"압축 파일 {zip_filepath} 생성 및 원본 파일 삭제 완료.")

        time.sleep(60)  # 60초마다 폴더 검사


# 사용 예시:
source_folder = "/content/Fooocus/outputs"  # 모니터링할 폴더 경로를 지정합니다.
destination_folder = "/content/drive/MyDrive/Loras/outputs"  # 압축 파일 저장할 폴더 경로를 지정합니다.

# 폴더가 존재하지 않으면 생성합니다.
#os.makedirs(source_folder, exist_ok=True)
#os.makedirs(destination_folder, exist_ok=True)


monitor_and_zip(source_folder, destination_folder)

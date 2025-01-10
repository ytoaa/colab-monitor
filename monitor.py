import os
import pyzipper
import time
import argparse

def monitor_and_zip(source_folder, destination_folder, threshold=1, file_types=('.webp', '.png', '.jpeg'), password=None, delete_delay=5, monitor_delay=10):
    """
    특정 폴더 및 하위 폴더를 모니터링하고, 지정된 파일 형식의 파일 개수가 threshold를 넘으면 파일들을 zip으로 압축하여 다른 폴더로 이동합니다.
    비밀번호를 설정할 수 있습니다.

    Args:
        source_folder: 모니터링할 폴더의 경로.
        destination_folder: 압축된 zip 파일을 저장할 폴더 경로.
        threshold: 파일 개수 임계값 (기본값: 1).
        file_types: 카운트할 파일 형식들의 튜플 (예: ('.webp', '.png', '.jpeg')).
        password: 압축 파일에 설정할 비밀번호 (없으면 비밀번호 없음).
        delete_delay: 파일 삭제 전 대기 시간 (초).
        monitor_delay: 모니터링 주기 (초).
    """
    while True:
        files_to_zip = []  # zip에 포함될 파일 목록 저장
        count = 0
        for root, _, files in os.walk(source_folder):
            for file in files:
                if file.lower().endswith(file_types):
                    file_path = os.path.join(root, file)
                    files_to_zip.append(file_path)  # 파일 경로 추가
                    count += 1

        if count >= threshold:
            source_folder_name = os.path.basename(source_folder)
            zip_filename = f"{source_folder_name}_{time.strftime('%Y%m%d%H%M%S')}.zip"
            zip_filepath = os.path.join(destination_folder, zip_filename)

            with pyzipper.AESZipFile(zip_filepath, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
                if password:
                    zipf.setpassword(password.encode('utf-8'))
                for file_path in files_to_zip:
                    zipf.write(file_path, arcname=os.path.relpath(file_path, source_folder))

            # zip에 포함된 파일 삭제
            time.sleep(delete_delay)
            for file_path in files_to_zip:
                try:
                    os.remove(file_path)
                    print(f"파일 '{file_path}' 삭제 완료")
                except OSError as e:
                    print(f"파일 '{file_path}' 삭제 실패: {e}")

            print(f"압축 파일 {zip_filepath} 생성 및 원본 파일 삭제 완료.")

        time.sleep(monitor_delay)

if __name__ == "__main__":
    # 명령줄 인수를 처리하기 위한 argparse 설정
    parser = argparse.ArgumentParser(description="모니터링하고 파일을 압축하는 스크립트입니다.")
    parser.add_argument("--source", required=True, help="모니터링할 폴더 경로")
    parser.add_argument("--destination", required=True, help="압축 파일 저장할 폴더 경로")
    parser.add_argument("--threshold", type=int, default=1, help="파일 개수 임계값 (기본값: 1)")
    parser.add_argument("--file_types", nargs='*', default=['.webp', '.png', '.jpeg'], help="대상 파일 확장자 리스트")
    parser.add_argument("--password", help="압축 파일에 설정할 비밀번호 (없으면 비밀번호 없음)")
    parser.add_argument("--delete_delay", type=int, default=5, help="파일 삭제 전 대기 시간 (초, 기본값: 5)")
    parser.add_argument("--monitor_delay", type=int, default=10, help="모니터링 주기 (초, 기본값: 10)")

    args = parser.parse_args()

    # 경로가 존재하지 않으면 생성
    os.makedirs(args.source, exist_ok=True)
    os.makedirs(args.destination, exist_ok=True)

    # 함수 호출
    monitor_and_zip(
        source_folder=args.source,
        destination_folder=args.destination,
        threshold=args.threshold,
        file_types=tuple(args.file_types),
        password=args.password,
        delete_delay=args.delete_delay,
        monitor_delay=args.monitor_delay
    )

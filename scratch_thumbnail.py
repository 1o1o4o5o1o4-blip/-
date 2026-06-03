import re
from IPython.display import Image, display

# --- 動作確認用のテストデータ（環境に合わせて書き換えてください） ---
choice = "project"
project_input_to_search = "https://mit.edu"
# -------------------------------------------------------------

if choice == "project":
    if not project_input_to_search:
        print(
            "エラー: プロジェクトIDまたはURLが設定されていません。フォームフィールドの 'project_input_to_search' を設定してください。"
        )
    else:
        project_user_input = project_input_to_search.strip()

        project_id = None
        final_image_url_to_fetch = None

        match_direct_image_url = re.search(
            r"(https://scratch\.mit\.edu/get_image/project/(\d+)_.*\.png)",
            project_user_input,
        )
        if match_direct_image_url:
            final_image_url_to_fetch = match_direct_image_url.group(1)
            project_id = match_direct_image_url.group(2)
        else:
            match_project_page = re.search(
                r"scratch\.mit\.edu/projects/(\d+)", project_user_input
            )
            if match_project_page:
                project_id = match_project_page.group(1)
            elif project_user_input.isdigit():
                project_id = project_user_input

        if project_id:
            final_image_url_to_fetch = f"https://scratch.mit.edu/get_i%6d%61ge/p%72oject/{project_id}_1000x1000.png"

        if final_image_url_to_fetch and project_id:
            print(f"\n--- プロジェクトID「{project_id}」の画像URL ---")
            display(Image(url=final_image_url_to_fetch))  # Display the image
            print(f"生成された画像URL: {final_image_url_to_fetch}")
            print(
                "注意: このURLは直接検証されていません。ブラウザで開いて確認してください。"
            )

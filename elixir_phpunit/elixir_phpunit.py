import os
import sys
import pandas as pd
import openai

def read_excel_file(file_path):
    # Excelファイルからシートを読み込む
    validations = pd.read_excel(file_path, sheet_name='Validations')
    page_items = pd.read_excel(file_path, sheet_name='Page_Items')
    return validations, page_items

def get_column_names(page_items):
    # 論理名と物理名の対応辞書を作成する
    column_mapping = dict(zip(page_items['論理名'], page_items['物理名']))
    return column_mapping

def interpret_validation_conditions(conditions, column_mapping):
    # ChatGPT APIを呼び出して条件を解釈する
    # FIXME:べた書きをやめる！！！
    openai.api_key = "API KEY"
    
    test_cases = []

    for condition in conditions:
        # Excelの各列の情報を取得
        logical_column_name = condition['対象列']
        physical_column_name = column_mapping.get(logical_column_name, logical_column_name)
        validation_condition = condition['バリデーション条件']
        error_message = condition['エラーメッセージ']

        # 読み取った内容からプロンプトを組み立てる
        # ブラウザ版のChatと変わらない回答が返ってくるので、テストコードだけを出力するよう要求しておく
        # ときどき解釈違いが発生するので、できたコードは必ず確認が必要。
        prompt = f"""
        Generate a PHPUnit test case for the following validation condition:
        - Column: {physical_column_name}
        - Condition: {validation_condition}
        - Error Message: {error_message}

        Please response only the test code and no other answers.

        Example:
        public function testValidationErrors()
        """

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        test_cases.append(response.choices[0].message.content.strip())

    return test_cases

def generate_test_code(test_cases):
    test_code = """
    <?php

    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Tests\TestCase;

    class ExcelImportValidationTest extends TestCase
    {
        use RefreshDatabase;
    """
    
    for test_case in test_cases:
        test_code += test_case + "\n"
    
    test_code += "\n}"

    # FIXME:文字コードの関係で日本語が文字化けする、、、あとコード形式のタグが付いてるのでそのまま使えない
    return test_code

def main(file_path=None):

    if file_path:
        # 引数で指定されたファイルパスが存在するかチェック
        if not os.path.isfile(file_path):
            print(f"Error: The file at {file_path} does not exist.")
            return None
    else:
        # 引数がない場合、スクリプトと同じディレクトリにある'validate.xlsx'を使用
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'validate.xlsx')
        
        if not os.path.isfile(file_path):
            print(f"Error: The default file validate.xlsx does not exist in the current directory.")
            return None

    try:
        # Excelファイルを読み込む
        validations, page_items = read_excel_file(file_path)
        column_mapping = get_column_names(page_items)
        conditions = validations.to_dict(orient='records')

        # ChatGPT APIを呼び出してバリデーション条件を解釈させる
        test_cases = interpret_validation_conditions(conditions, column_mapping)
        # ChatGPTからのレスポンスをテストコードにする
        test_code = generate_test_code(test_cases)
        with open('ExcelImportValidationTest.php', 'w') as file:
            file.write(test_code)   

    except Exception as e:
        print(f"Failed to Generate Test Code. Error: {e}")
        return None
    
if __name__ == "__main__":
    # コマンドライン引数をチェック（1つ目の引数をファイルパスとして使用）
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    main(file_path)

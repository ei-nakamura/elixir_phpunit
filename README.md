# elixir_phpunit  
Excelに記載されたバリデーション条件を読み取り、ChatGPT APIを用いてバリデーション内容を解釈しPHPUnit化するスクリプトです。  
あまりにも現職の品質が悪すぎるため、まず自動テストをどうにかしようとして作成しましたが日の目を見ていません、、、  
  
ちなみに、このソース自体もほとんどChatGPT 4oに書かせています。  
Advanced Technology Unitという社内のチームにて急遽発表することになり、せっかくなのでAIに任せてみることにしました。  
当然、そのままでは動かなかったので手を入れてはいますが、大まかなロジックは出力されたほぼそのままです。 
https://chatgpt.com/share/ef83d8a2-86d5-4084-84c5-58b172322ef5  
  
使用言語：python, php  
実行コマンド：python elixir_phpunit.py 読み込み対象のExcelファイルパス(省略可)  
実行すると、./ExcelImportValidationTest.phpにChatGPTで生成されたテストコードが出力されます。

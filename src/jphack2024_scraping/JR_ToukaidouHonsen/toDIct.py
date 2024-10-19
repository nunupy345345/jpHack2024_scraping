import re

# 入力文字列
content = """
# JR東海道本線
# ['/station-guide/shinkansen/atami/index.html', '/station-guide/shizuoka/kannami/index.html', ...]
# 飯田線
# ['/station-guide/shinkansen/toyohashi/index.html', '/station-guide/tokai/toyokawa/index.html', ...]
# 中央本線
# ['/station-guide/shinkansen/nagoya/index.html', '/station-guide/tokai/kanayama/index.html', ...]
# 武豊線
# ['/station-guide/tokai/obu/index.html', '/station-guide/tokai/ogawa/index.html', ...]
# 太多線
# ['/station-guide/tokai/tajimi/index.html', '/station-guide/tokai/kani/index.html', ...]
# 関西本線
# ['/station-guide/shinkansen/nagoya/index.html', '/station-guide/tokai/hatta/index.html', ...]
# 高山本線
# ['/station-guide/tokai/gifu/index.html', '/station-guide/tokai/unuma/index.html', ...]
# 参宮線
# ['/station-guide/tokai/taki/index.html', '/station-guide/tokai/iseshi/index.html']
# 紀勢本線
# ['/station-guide/tokai/kameyama/index.html', '/station-guide/tokai/tsu/index.html', ...]
# 名松線
# ['/station-guide/tokai/matsusaka/index.html']
"""

# 正規表現を使用して路線名とURLリストを抽出
pattern = r'#\s+(.*?)\n#\s+(\[.*?\])'
matches = re.findall(pattern, content, re.DOTALL)

# 結果を格納する辞書
result = {}

# 抽出した情報を辞書に格納
for line_name, urls in matches:
    # URLリストを文字列から実際のリストに変換
    url_list = eval(urls)
    result[line_name] = url_list

# 結果を整形して出力
output = "{\n"
for line, urls in result.items():
    output += f'    "{line}": {urls},\n'
output = output.rstrip(',\n') + "\n}"

print(output)
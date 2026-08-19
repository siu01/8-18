from git import Repo
import subprocess
import os
import glob
import xml.etree.ElementTree as ET

repo = Repo("./lucene")

branch_name = "feature/test"

if branch_name in [head.name for head in repo.heads]:
    branch = repo.heads[branch_name]
else:
    branch = repo.create_head(branch_name)

branch.checkout()

print("現在のブランチ:", repo.active_branch.name)

# ==========================================
# Gradle Wrapper を絶対パスで指定
# ==========================================

if os.name == "nt":
    gradle_command = os.path.join(
        repo.working_tree_dir,
        "gradlew.bat"
    )
else:
    gradle_command = os.path.join(
        repo.working_tree_dir,
        "gradlew"
    )

print("Gradle:", gradle_command)
print("存在:", os.path.exists(gradle_command))

result = subprocess.run(
    [gradle_command, "test"],
    cwd=repo.working_tree_dir,
    capture_output=True,
    text=True
)

print("終了コード:", result.returncode)

print("===== Gradle Output =====")
print(result.stdout)

print("===== Gradle Error =====")
print(result.stderr)

if result.returncode == 0:
    print("BUILD SUCCESS")
else:
    print("BUILD FAILURE")


# ==========================================
# XMLテスト結果を探す
# ==========================================

report_pattern = os.path.join(
    repo.working_tree_dir,
    "**",
    "build",
    "test-results",
    "test",
    "TEST-*.xml"
)

xml_files = glob.glob(
    report_pattern,
    recursive=True
)

print()
print("XMLファイル数:", len(xml_files))

total_tests = 0
total_failures = 0
total_errors = 0
total_skipped = 0

for xml_file in xml_files:

    tree = ET.parse(xml_file)
    root = tree.getroot()

    tests = int(root.attrib.get("tests", 0))
    failures = int(root.attrib.get("failures", 0))
    errors = int(root.attrib.get("errors", 0))
    skipped = int(root.attrib.get("skipped", 0))

    total_tests += tests
    total_failures += failures
    total_errors += errors
    total_skipped += skipped

    print("=" * 80)
    print("XML:", xml_file)
    print("テスト数:", tests)
    print("失敗:", failures)
    print("エラー:", errors)
    print("スキップ:", skipped)

print()
print("===== 合計 =====")
print("テスト数:", total_tests)
print(
    "成功:",
    total_tests
    - total_failures
    - total_errors
    - total_skipped
)
print("失敗:", total_failures)
print("エラー:", total_errors)
print("スキップ:", total_skipped)
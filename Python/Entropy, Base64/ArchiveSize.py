from os import stat
Result = "\n\nРозмір архівів:\n"
for form in ["7z","rar","tar.bz2","tar.gz","zip"]:
    for i in range(1,4):
        File_name = f"{i}.{form}"
        File_size = stat(File_name).st_size
        Result += f" {File_name}: {File_size} Б\n"
res = open("Archives-Size.txt", 'a', encoding="utf-8")
res.write(Result)
res.close()
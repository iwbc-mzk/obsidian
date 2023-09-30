import yaml
import shutil
import os

PREFERENCE_DIR = ".mkdocs"
DOCKS_DIR = "docs"

os.makedirs(DOCKS_DIR, exist_ok=True)
os.makedirs(f"{DOCKS_DIR}/scripts", exist_ok=True)

# 参考元
# https://tick-taku.com/blog/obsidian_mkdocs_githubactions_netlify_snk/#mkdocs-html
with open(f"{PREFERENCE_DIR}/conf.yml") as conf_file:
    conf = yaml.safe_load(conf_file)
    shutil.copy(f"{PREFERENCE_DIR}/mkdocs.yml", "./")

    if "index" in conf:
        index = conf["index"]
        shutil.copy(index, f"{DOCKS_DIR}/{os.path.basename(index)}")

    if "logo" in conf:
        logo = conf["logo"]
        shutil.copy(logo, f"{DOCKS_DIR}/{os.path.basename(logo)}")

    if "favicon" in conf:
        favicon = conf["favicon"]
        shutil.copy(favicon, f"{DOCKS_DIR}/{os.path.basename(favicon)}")

    if "custom_theme" in conf:
        theme = conf["custom_theme"]
        shutil.copytree(f"{PREFERENCE_DIR}/{theme}", theme, dirs_exist_ok=True)

    for doc in conf["docs"]:
        shutil.copytree(doc, f"{DOCKS_DIR}/{doc}", dirs_exist_ok=True)

    if "files" in conf:
        for file in conf["files"]:
            shutil.copytree(file, f"{DOCKS_DIR}/{os.path.basename(file)}")
    
    if "scripts" in conf:
        for script in conf["scripts"]:
            shutil.copy(f"{PREFERENCE_DIR}/scripts/{script}", f"{DOCKS_DIR}/scripts/{os.path.basename(script)}")

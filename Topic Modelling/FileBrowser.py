import os
import re
import errno

#pathDoc = '../wiki_en-20160113'
#pathModel = "/Volumes/My Passport/gensim-wiki-ensimple-20160111"

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def returnFilePathsFromDirectory(pathDoc):
    articles = []
    if os.path.isdir(pathDoc):
        for (path, dirs, files) in os.walk(pathDoc):
            for fil in files:
                if(not str(fil).startswith('.')):
                    articles.append(str(path)+'/'+str(fil))
        return sorted(articles)
    else:
        articles.append(pathDoc)
        return articles

def returnFilePathsFromDirectoryLevel(pathDoc, level=1):
    articles = []
    if os.path.isdir(pathDoc):
        for (path, dirs, files) in os.walk(pathDoc):
            for fil in files:
                if (not str(fil).startswith('.')):
                    articles.append(str(path) + '/' + str(fil))
            level-=1
            if level <= 0:
                break
        return sorted(articles)
    else:
        articles.append(pathDoc)
        return articles

def returnArticles(pathDoc):
    articles = []

    os.chdir(pathDoc)
    list = os.listdir(os.curdir)

    for dir in list:

        if os.path.isdir(dir):
            sublist = filter(lambda f: not f.startswith('.'), os.listdir(dir))
            articles.extend(sublist)
            # return articles

    return articles

def returnAllDirs(path_doc):
    directories = []
    for (path, dirs, files) in os.walk(path_doc):
        for dir in sorted(dirs):
            #if(not str(fil).startswith('.')):
            directories.append(str(path)+'/'+str(dir))
    return directories


def countArticles(path):
    f = open(path)
    line = f.readline()
    count = 0;
    while line:
        # assume there's one document per line, tokens separated by whitespace
        # yield dictionary.doc2bow(line.lower().split())
        startLinePattern = re.compile("<doc.*>")
        endlinePattern = re.compile("</doc>")
        if startLinePattern.match(line):
            count + 1
    f.close()

def countArticleHierarchy(list):
    for path in list:
        f = open(path)
        line = f.readline()
        count = 0;
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())
            startLinePattern = re.compile("<doc.*>")
            endlinePattern = re.compile("</doc>")
            if startLinePattern.match(line):
                count + 1
        f.close()

def returnModelsWithEnding(list ,pathModel):
    articles = []
    if os.path.isdir(pathModel):
        for (path, dirs, files) in os.walk(pathModel):
            for fil in files:
                for s in list:
                    if(not str(fil).startswith('.') and str(fil).endswith(s)):
                        articles.append(str(path)+'/'+str(fil))
        return articles
    else:
        articles.append(pathModel)
        return articles

def create_folder_if_not_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def returnFilesWithEnding(pathModel, ending):
    articles = []
    if os.path.isdir(pathModel):
        for (path, dirs, files) in os.walk(pathModel):
            for fil in files:
                if(not str(fil).startswith('.') and str(fil).endswith(ending)):
                    articles.append(str(path)+'/'+str(fil))
        return articles
    else:
        articles.append(pathModel)
        return articles

def file_exists(path_file):
    return os.path.isfile(path_file)
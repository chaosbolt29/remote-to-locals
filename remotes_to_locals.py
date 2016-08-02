import optparse
import os
import time

def all_files(directory):
    for path, dirs, files in os.walk(directory):
        for f in files:
            yield os.path.join(path, f)

def main():

    parser = optparse.OptionParser('usage ./program -m <full path directory to find html files> -f <filetype>')
    parser.add_option('-m', dest='maindir', type='string', help='the program will crawl all html files in all subfolders')
    parser.add_option('-f', dest='filetype', type='string', help='if left empty, filetype is html')
    (options, args) = parser.parse_args()

    working_directory = options.maindir
    filetype = options.filetype

    if working_directory == None:
        print parser.usage
        exit(0)
    if filetype == None:
        filetype = 'html'

    print 'crawling all files and folders in search of .' + filetype + ' files ...\n'

    file_list = [f for f in all_files(working_directory) if f.endswith(filetype)]

    os.system('mkdir -p ' + working_directory + 'assets/images')
    os.system('mkdir -p ' + working_directory + 'assets/js')
    os.system('mkdir -p ' + working_directory + 'assets/css')
    # this creates the images, css, js folders where the dowloaded files will be placed
    ftype = None

    for f in file_list:   # iterates through all the files in this directory and subdirectories

        path_decomposed = f.split('/')[1:]
        print f + '\n'

        file_length = len(path_decomposed)
        rel_depth = file_length - 6

        grep_regex_cmd = 'cat ' + f + ' | grep -Eo "(http|https|)(:|)//[a-zA-Z0-9./?=_-]*(css|js|png|jpeg|jpg|ico|gif)" | sort | uniq'

        #this grep uses regex to find all downloadable css, js, png, jpeg, etc... in the file

        tmp = os.popen(grep_regex_cmd).read()
        dl_list = tmp.split('\n')   # a list of the downloadable files URLs
        print dl_list

        for dl_f in dl_list[:-1]: # loop through all but last element (that contains nothing)

            if 'html5shim' in dl_f or 'googletagmanager' in dl_f:
                 continue

            tmp_list = dl_f.split('/')  # splits the url by /

            if tmp_list[-1].endswith('css'):
                ftype = 'css'
            if tmp_list[-1].endswith('js'):
                ftype = 'js'
            if tmp_list[-1].endswith('gz.css'):
                tmp_list[-1] = tmp_list[-1][0:-6] + 'css'
                ftype = 'css'
            if tmp_list[-1].endswith('gz.css'):
                tmp_list[-1] = tmp_list[-1][0:-5] + 'css'
                ftype = 'css'
            if tmp_list[-1].endswith('jpeg') or tmp_list[-1].endswith('jpg') or tmp_list[-1].endswith('png') or tmp_list[-1].endswith('ico') or tmp_list[-1].endswith('gif'):
                ftype = 'images'
            if ftype == None:
                print 'not a valid type\n'
                continue

            if rel_depth == 0:
                local_f = 'assets/' + ftype + '/'
            if rel_depth > 0:
                local_f = '../'*rel_depth + 'assets/' + ftype + '/'

            #print 'Downloading ' + ftype + ' file : ' + tmp_list[-1] + ' :new html source ' + local_f + '\n'
            pref = ''
            if dl_f.startswith('http'):
                pref = ''
            else:
                pref = 'http:'

            wget_cmd = 'wget -nc -P ' + working_directory + 'assets/' + ftype + '/ -U mozilla ' + pref + dl_f
            try:
                os.system(wget_cmd)
            except:
                pass


            print 'replacing urls with local files'
            sed_cmd = "sed -i -e 's," + dl_f + "," + local_f + tmp_list[-1] + ",g' " + f
            try:
                os.system(sed_cmd)
            except:
                pass


if __name__ == '__main__':
    main()

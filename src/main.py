import argparse
import os
import subprocess
import json
from pdf_stuff import get_pdfs, combine_pdfs
from path_stuff import make_abs

def main():
    args = parse()
    with open(args['config_file'], 'r') as f:
        config = json.load(f)
    pdf_list = get_pdfs(args['input_directory'])
    if args['exclusions']:
        pdf_list = sub_lists(pdf_list, args['exclusions'])
    filename = combine_pdfs(pdf_list, args['output-filename'], args['input_directory'])
    filename = os.path.join(args['input_directory'], filename)
    to_epub(filename, args['output_directory'], args['title'], args['author'], config)



def parse():
    parser = argparse.ArgumentParser(prog="comic-compiler", description="compiles multiple pdf files into a comic in epub format")
    parser.add_argument("output-filename", type=str)
    parser.add_argument("-i", "--input-directory", type=str, default=os.getcwd())
    parser.add_argument("-c", "--config-file", type=str, default="config.json")
    parser.add_argument("-o", "--output-directory", type=str, default=os.getcwd())
    parser.add_argument("-e", "--exclusions", nargs='*')
    parser.add_argument("-t", "--title", type=str, required=True)
    parser.add_argument("-a", "--author", type=str, required=True)

    args = vars(parser.parse_args())
    if args['input_directory'] is not os.getcwd():
        args['input_directory'] = os.path.abspath(args['input_directory'])
    if args['input_directory'].endswith('"'):
        args['input_directory'] = args['input_directory'][0:len(args['input_directory']) - 1] + "\\"
    if args['output_directory'] is not os.getcwd():
        args['output_directory'] = os.path.abspath(args['output_directory'])
    if args['output_directory'].endswith('"'):
        args['output_directory'] == args['output_directory'][0:len(args['output_directory']) - 1] + "\\"
    if os.path.dirname(__file__) is not os.getcwd:
        args['config_file'] = os.path.join(os.path.dirname(__file__), args['config_file'])
    if args['exclusions']:
        args['exclusions'] = make_abs(args['exclusions'])
    
    return args

def sub_lists(list1, list2):
    if list2 > list1:
        raise Exception("Cannot subtract bigger list from smaller list.")
    list3 = []

    for item1 in list1:
        if item1 in list2:
            continue
        else:
            list3.append(item1)
    return list3

def to_epub(pdf_file, output_path, title, author, config):
    print(pdf_file)
    dir = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    cmd = ['.\\KCC_c2e_7.3.3.exe']
    profile = config['kcc-profile']
    height = config['height']
    width = config['width']
    force_color = config['force-color']
    manga_mode = config['manga-mode']
    webtoon_mode = config['webtoon-mode']
    stretch = config['stretch']
    upscale = config['upscale']
    disable_processing = config['disableProcessing']
    cmd.append(pdf_file)
    cmd.append('-p')
    cmd.append(profile)
    if manga_mode:
        cmd.append('-m')
    elif webtoon_mode:
        cmd.append('-w')

    if upscale:
        cmd.append('-u')
    if stretch:
        cmd.append('-s')
    if force_color:
        cmd.append('--forcecolor')
    if width != 0:
        cmd.append('--customwidth')
        cmd.append(f'{width}')
    if height != 0:
        cmd.append('--customheight')
        cmd.append(f'{height}')
    if disable_processing:
        cmd.append('--noprocessing')
    cmd.append('-o')
    cmd.append(output_path)
    cmd.append('-t')
    cmd.append(title)
    cmd.append('-a')
    cmd.append(author)
    cmd.append('-f')
    cmd.append('EPUB')
    cmd.append('--nokepub')

    subprocess.run(cmd)
    os.chdir(dir)

if __name__ == '__main__':
    main()
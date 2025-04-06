import argparse
import os
import json
import sys
from .pdf_stuff import get_pdfs, combine_pdfs
from .path_stuff import make_abs
from .utils.paths import *

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
        args['input_directory'] = args['input_directory'][0:len(args['input_directory']) - 1] + os.pathsep
    if args['output_directory'] is not os.getcwd():
        args['output_directory'] = os.path.abspath(args['output_directory'])
    if args['output_directory'].endswith('"'):
        args['output_directory'] == args['output_directory'][0:len(args['output_directory']) - 1] + os.pathsep
    args['config_file'] = os.path.join(config_dir(), args['config_file'])
    if args['exclusions']:
        args['exclusions'] = make_abs(args['exclusions'])
    
    return args

def sub_lists(list1, list2):
    if list2 > list1:
        raise Exception("Cannot subtract bigger list from smaller list.")
    list3 = []

    for item in list1:
        if item in list2:
            continue
        else:
            list3.append(item)
    return list3

def to_epub(pdf_file, output_path, title, author, config):
    cmd = [r" ¯\_(ツ)_/¯"]
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
    sys.argv = cmd
    call_kcc()

def call_kcc():
    from .external.kcc.kcc import modify_path

    if sys.version_info < (3, 8, 0):
        print('ERROR: This is a Python 3.8+ script!')
        sys.exit(1)
    from multiprocessing import freeze_support, set_start_method
    from .external.kcc.kindlecomicconverter.startup import startC2E

    modify_path()
    set_start_method('spawn')
    freeze_support()
    startC2E()

if __name__ == '__main__':
    main()
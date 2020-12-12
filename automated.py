import ast, astor
import random
import sys
from FindHelper import *
import Refactoring
import astpretty
import colorama

import fitness


def populate(fname, output_file, astree, rtype, pcls):
    print("populate {}, {}".format(rtype, pcls.name))
    refactorings = set()
    if rtype == "PushDownMethod":
        methods = find_all_methods(pcls)
        for method in methods:
            refactorings.add(
                Refactoring.PushDownMethod(
                    fname, astree, pcls, method, output_file=output_file
                )
            )
    if rtype == "PullUpMethod":
        methods = find_all_methods(pcls)
        for method in methods:
            refactorings.add(
                Refactoring.PullUpMethod(
                    fname, astree, pcls, method, output_file=output_file
                )
            )
    return refactorings


def update_metric_log():
    print("update metric log")


def run(input_file: str, output_file: str):
    astree = astor.parse_file(input_file)
    desired_refactoring_count = 100
    refactoring_count = 0
    while refactoring_count < desired_refactoring_count:
        classes = set([node for node in find_all_classes(astree)])
        while len(classes) > 0:
            picked_class = random.sample(classes, 1)[0]
            classes.remove(picked_class)
            # refactoring_types = set([ "PullUpMethod", "PushDownMethod", "PullUpField", "PushDownField" ])
            refactoring_types = set(["PullUpMethod", "PushDownMethod"])
            while len(refactoring_types) > 0:
                picked_refactoring_type = random.sample(refactoring_types, 1)[0]
                print(picked_refactoring_type)
                refactoring_types.remove(picked_refactoring_type)
                refactorings = populate(
                    fname=input_file,
                    output_file=output_file,
                    astree=astree,
                    rtype=picked_refactoring_type,
                    pcls=picked_class,
                )
                if len(refactorings) > 0:
                    refactoring = random.sample(refactorings, 1)[0]
                    refactoring.apply()
                    # refactoring.undo()
                    # if fitness_function_improves():
                    #     refactoring_count += 1
                    #     update_metric_log()
                    #     Todo: refactored file read and write to original file
                    # else:
                    #     refactoring.undo()
        break


if __name__ == "__main__":
    colorama.init()
    Fore = colorama.Fore
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    score_before = fitness.compute_project_score(input_file)
    print(Fore.YELLOW + "Before:", score_before, Fore.RESET)
    run(input_file, output_file)
    score_after = fitness.compute_project_score(output_file)
    print(Fore.YELLOW + "After:", score_after, Fore.RESET)

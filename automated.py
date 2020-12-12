import shutil

import ast, astor
import random
import sys
from FindHelper import *
import Refactoring
import astpretty
import colorama

import fitness


colorama.init()
Fore = colorama.Fore


def populate(fname, rtype, pcls):
    print("populate {}, {}".format(rtype, pcls.name))
    refactorings = set()
    if rtype == "PushDownMethod":
        methods = find_all_methods(pcls)
        for method in methods:
            refactorings.add(
                Refactoring.PushDownMethod(
                    fname=fname,
                    src_cls=pcls,
                    target=method,
                )
            )
    if rtype == "PullUpMethod":
        methods = find_all_methods(pcls)
        for method in methods:
            refactorings.add(
                Refactoring.PullUpMethod(
                    fname=fname,
                    src_cls=pcls,
                    target=method,
                )
            )
    return refactorings


def update_metric_log():
    print("update metric log")


def tcc_improvement_check(before_file: str, after_file: str) -> float:
    """Return the change in TCC score between two files."""
    before_score = fitness.compute_project_score(before_file)
    after_score = fitness.compute_project_score(after_file)
    return after_score.tcc - before_score.tcc


def run(input_file: str, output_file: str):
    # input_file을 output_file로 미리 복사한다.
    # 그러면 input_file은 건드리지 않고 output_file을 자유롭게 갖고 놀 수 있다.
    shutil.copyfile(input_file, output_file)

    desired_refactoring_count = 100
    refactoring_count = 0
    while refactoring_count < desired_refactoring_count:
        astree = astor.parse_file(output_file)
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
                    fname=output_file,
                    rtype=picked_refactoring_type,
                    pcls=picked_class,
                )
                if len(refactorings) > 0:
                    refactoring = random.choice(list(refactorings))

                    before_score = fitness.compute_project_score(output_file)

                    refactoring.read_file()
                    refactoring.apply()
                    refactoring.write_file()

                    after_score = fitness.compute_project_score(output_file)
                    # refactoring.undo()
                    lcc_score_change = after_score.lscc - before_score.lscc
                    if lcc_score_change >= 0:
                        print(f"{Fore.GREEN}LSCC score improved: {lcc_score_change}{Fore.RESET}")
                        refactoring_count += 1
                        update_metric_log()
                        # Todo: refactored file read and write to original file
                    else:
                        print(f"{Fore.GREEN}LSCC score not improved: {lcc_score_change}{Fore.RESET}")
                        refactoring.undo()
        break


#
# A -> Z
#  ----------
#  현재 상황: refactoring종류가 PullUPMethod, PullDownMethod, ...
#  input file A 이고 output file B라고 하자.
#
# run()은 A를 읽어서 astree를 만든다.
#
#   refactor1을 실행하면 astree를 고친 다음 Z에 저장한다.
#   refactor2을 실행하면 astree를 고친 다음 Z에 저장한다.
#
# 바꾼다면...??
#
#   처음에 run()이 A를 읽어서 Z에 복사한다. (리팩토링은 아직 미적용)
#   refactor1을 실행하면 Z를 읽어서 고친 다음 Z에 저장한다. 이때 고치기 전의 내용을 기억한다. (히스토리 1)
#   refactor2을 실행하면 Z를 읽어서 고친 다음 Z에 저장한다. 이때 고치기 전의 내용을 기억한다. (히스토리 2)
#   refactor2에 대해 undo()를 해야 한다면 히스토리 2를 불러와서 다시 Z에 저장한다.

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    score_before = fitness.compute_project_score(input_file)
    print(Fore.YELLOW + "Before:", score_before, Fore.RESET)
    run(input_file, output_file)
    score_after = fitness.compute_project_score(output_file)
    print(Fore.YELLOW + "After:", score_after, Fore.RESET)

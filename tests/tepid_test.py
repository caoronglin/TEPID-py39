#!/usr/bin/env python3

import random
import shutil
import string
from pathlib import Path

from tepid import tepid


TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
ANNOTATION = PROJECT_ROOT / "Annotation" / "Arabidopsis" / "TAIR9_TE.bed.gz"


class Args:
    pass


def _copy_test_inputs(tmp_path):
    for name in [
        "conc.bam",
        "conc.bam.bai",
        "split.bam",
        "conc_empty.bam",
        "conc_empty.bam.bai",
        "split_empty.bam",
        "split_empty.bam.bai",
    ]:
        shutil.copy2(TESTS_DIR / name, tmp_path / name)


def _discover_args(tmp_path, name, conc, split):
    args = Args()
    args.keep = True
    args.deletions = False
    args.insertions = False
    args.strict = False
    args.mask = ""
    args.discordant = False
    args.proc = 1
    args.name = name
    args.conc = str(tmp_path / conc)
    args.split = str(tmp_path / split)
    args.te = str(ANNOTATION)
    args.prefix = (
        "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        + "_"
    )
    return args


def test_discover_pe(tmp_path, monkeypatch):
    _copy_test_inputs(tmp_path)
    monkeypatch.chdir(tmp_path)

    discover = _discover_args(tmp_path, "run", "conc.bam", "split.bam")
    tepid.discover_pe(discover)

    test_ins = (tmp_path / "insertions_run.bed").read_text().splitlines(keepends=True)
    true_ins = (TESTS_DIR / "insertions_test.bed").read_text().splitlines(keepends=True)
    test_del = (tmp_path / "deletions_run.bed").read_text().splitlines(keepends=True)
    true_del = (TESTS_DIR / "deletions_test.bed").read_text().splitlines(keepends=True)

    assert test_ins == true_ins
    assert test_del == true_del


def test_discover_pe_empty_output(tmp_path, monkeypatch):
    _copy_test_inputs(tmp_path)
    monkeypatch.chdir(tmp_path)

    empty = _discover_args(tmp_path, "run", "conc_empty.bam", "split_empty.bam")
    assert tepid.discover_pe(empty) == 1, "Empty output test failed"


def test_discover_pe_reuses_output_names_without_cross_run_pollution(
    tmp_path, monkeypatch
):
    _copy_test_inputs(tmp_path)
    monkeypatch.chdir(tmp_path)

    discover = _discover_args(tmp_path, "run", "conc.bam", "split.bam")
    tepid.discover_pe(discover)

    empty = _discover_args(tmp_path, "run", "conc_empty.bam", "split_empty.bam")
    assert tepid.discover_pe(empty) == 1, "Sequential empty output test failed"

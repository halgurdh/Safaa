#!/usr/bin/env vpython3
#
# Copyright (c) 2023 The Brave Authors. All rights reserved.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at https://mozilla.org/MPL/2.0/. */


def remap_build_number(build_number):
    # Starting from Chromium's build number 5750 there is a change how
    # we generate version codes in order to provide proper app version
    # to the intel devices that support arm as well. Since we patch
    # build number with our version, we need to remap it.
    # We want to introduce this change starting from 1.53.x.
    if build_number >= 53:
        build_number = 5750
    return build_number


# Minor version (build_number) of Safaa's first Google Play release.
_FIRST_PLAY_MINOR = 100


def generate_base_version_code(build_number, patch_number):
    # Version codes are laid out as M_PPP_CD where M counts minor versions
    # (build_number) from _FIRST_PLAY_MINOR, PPP is patch_number, and CD is
    # the package/ABI suffix, e.g. 1.100.5 on arm64 is 100504. Brave's 42/43
    # prefix started Safaa at 430000004, which Google Play rejects as a jump
    # that would exhaust the 2100000000 versionCode limit; small codes leave
    # room for every future release.
    assert build_number >= _FIRST_PLAY_MINOR, (
        'Safaa version codes start at 1.%d.0' % _FIRST_PLAY_MINOR)
    assert patch_number < 1000, 'patch number must fit in 3 digits'
    return ((build_number - _FIRST_PLAY_MINOR + 1) * 1000 + patch_number) * 100

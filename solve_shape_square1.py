#!/usr/bin/env python3

__copyright__ = '''\
Copyright (C) Volker Diels-Grabsch <v@njh.eu>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

def solved_state():
    return ((2,1,2,1),(2,1,2,1)),((2,1,2,1),(2,1,2,1))

def string_of_quarter(q):
    return ''.join(str(v) for v in q)

def string_of_state(state):
    ((ul, ur), (ll, lr)) = state
    return '%s:%s,%s:%s' % (string_of_quarter(ul), string_of_quarter(ur), string_of_quarter(ll), string_of_quarter(lr))

def split_combined_half(combined):
    sum_half = 6
    sum_left = 0
    for i in range(len(combined)):
        sum_left += combined[i]
        if sum_left < sum_half:
            continue
        if sum_left == sum_half:
            return (combined[:i+1], combined[i+1:])
        return None

def rotate_half_to_left(half):
    (hl, hr) = half
    initial_combined = hl + hr
    combined = initial_combined
    while True:
        combined = combined[1:] + (combined[0],)
        if combined == initial_combined:
            return half
        split_result = split_combined_half(combined)
        if split_result is not None:
            return split_result

def ru(state):
    (uh, lh) = state
    return (rotate_half_to_left(uh), lh)

def rl(state):
    (uh, lh) = state
    return (uh, rotate_half_to_left(lh))

def sw(state):
    ((ul, ur), (ll, lr)) = state
    return ((ll, ur), (ul, lr))

def initial_space():
    return [[('in', solved_state())]]

def ops():
    return ((f.__name__, f) for f in (ru, rl, sw))

def add_level(space, visited_states):
    new_level = []
    for (prev_op, prev_state) in space[-1]:
        for op, op_func in ops():
            new_state = op_func(prev_state)
            if new_state not in visited_states:
                new_level.append((op, new_state))
                visited_states.add(new_state)
                print('%02d: %s <-(%s)- %s' % (len(space), string_of_state(new_state), op, string_of_state(prev_state)))
    space.append(new_level)

def evolve(space):
    visited_states = {state for level in space for (op, state) in level}
    for i in range(22):
        add_level(space, visited_states)

def main():
    space = initial_space()
    evolve(space)

main()

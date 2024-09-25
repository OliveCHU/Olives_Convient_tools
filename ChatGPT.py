#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 18:09:59 2023

@author: mengyuanchu
"""

from steamship import Steamship
ship = Steamship()
gpt4 = ship.use_plugin("gpt-4")
task = gpt4.generate(text="Tell me about Hong Kong ")
task.wait()
print(task.output.blocks[0].text)

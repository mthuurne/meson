# Copyright 2019 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This class contains the basic functionality needed to run any interpreter
# or an interpreter-based tool

from . import AstVisitor
from .. import mparser

class AstIndentationGenerator(AstVisitor):
    def __init__(self):
        self.level = 0

    def visit_default_func(self, node: mparser.BaseNode):
        # Store the current level in the node
        node.level = self.level

    def visit_ArrayNode(self, node: mparser.ArrayNode):
        self.visit_default_func(node)
        self.level += 1
        node.args.accept(self)
        self.level -= 1

    def visit_DictNode(self, node: mparser.DictNode):
        self.visit_default_func(node)
        self.level += 1
        node.args.accept(self)
        self.level -= 1

    def visit_MethodNode(self, node: mparser.MethodNode):
        self.visit_default_func(node)
        node.source_object.accept(self)
        self.level += 1
        node.args.accept(self)
        self.level -= 1

    def visit_FunctionNode(self, node: mparser.FunctionNode):
        self.visit_default_func(node)
        self.level += 1
        node.args.accept(self)
        self.level -= 1

    def visit_ForeachClauseNode(self, node: mparser.ForeachClauseNode):
        self.visit_default_func(node)
        self.level += 1
        node.items.accept(self)
        node.block.accept(self)
        self.level -= 1

    def visit_IfClauseNode(self, node: mparser.IfClauseNode):
        self.visit_default_func(node)
        for i in node.ifs:
            i.accept(self)
        if node.elseblock:
            self.level += 1
            node.elseblock.accept(self)
            self.level -= 1

    def visit_IfNode(self, node: mparser.IfNode):
        self.visit_default_func(node)
        self.level += 1
        node.condition.accept(self)
        node.block.accept(self)
        self.level -= 1

class AstIDGenerator(AstVisitor):
    def __init__(self):
        self.counter = {}

    def visit_default_func(self, node: mparser.BaseNode):
        name = type(node).__name__
        if name not in self.counter:
            self.counter[name] = 0
        node.ast_id = name + '#' + str(self.counter[name])
        self.counter[name] += 1

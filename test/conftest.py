# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-04-15 12:33:32
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-04-15 13:31:37
import pytest
from src.util import SyntexTreeGenerator
from .testConfig import expString


@pytest.fixture()
def expression(request):
    fineExpressions = [SyntexTreeGenerator.Expression(exp) for exp in expString['fineCases']]
    badExpressions = [SyntexTreeGenerator.Expression(exp) for exp in expString['badCases']]

    return {'fineExpressions': fineExpressions,
            'badExpressions': badExpressions
            }

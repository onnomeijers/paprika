from paprika.system.DictExt import DictExt


class ExpressionParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(expressions, dictionary):
        """
        Returns the evaluation of expressions against the given dictionary (locals)
        :param expressions:
        :param dictionary:
        :return:
        """
        if isinstance(expressions, list):
            result = []
            for expression in expressions:
                item = dict()
                for key in expression.keys():
                    if expression[key].startswith('#'):
                        item[key] = DictExt.dot(expression[key][1::], dictionary)
                    else:
                        item[key] = expression[key]
                result.append(item)
            return result
        if isinstance(expressions, dict):
            item = dict()
            for key in expressions.keys():
                if expressions[key].startswith('#'):
                    item[key] = DictExt.dot(expressions[key][1::], dictionary)
                else:
                    item[key] = expressions[key]
            return item

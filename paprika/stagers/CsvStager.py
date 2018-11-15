from paprika.repositories.Repository import Repository
from paprika.stagers.Csv import Csv


class Stager(Repository):
    def __init__(self, datasource):
        Repository.__init__(self, datasource)

    def stage(self, filename, header, delimiter, table_name, mapping, skip_header, statics=None):
        r = open(filename, 'rb')
        connection = self.get_connection()
        i = 0
        for line in r:
            if (not i == 0 and skip_header) or not skip_header:
                result = Csv.to_json(line, header, delimiter)

                # add statics if present
                if statics:
                    for key in statics.keys():
                        result[key] = "'" + str(statics[key]) + "'"

                # map
                fields = []
                values = []
                mapping_list = mapping.split(';')
                for m in mapping_list:
                    source, target = m.split('.')
                    fields.append(target)
                    values.append(result[source])

                # create dynamic sql statement
                statement = "insert into " + table_name + '(' + ', '.join(fields) + ')' + ' values (' + ", ".join(values) + ')'
                print statement
                cursor = connection.cursor()
                cursor.execute(statement)
                connection.commit()
            i += 1
        r.close()
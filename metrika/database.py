
import os.path
import yaml


class Database:
    def __init__(self, testbed):
        self.testbed = testbed
        self.filename = 'results-' + testbed + '.txt'
        self.results = self.load()

    def load(self):
        if not os.path.isfile(self.filename):
            return {}
        with open(self.filename, 'r+') as f:
            return eval(f.read())
#            return yaml.load(f)

    def save(self, new_results):
        for experiment, experiment_results in new_results.items():

            if experiment.name not in self.results.keys():
                self.results[experiment.name] = {}

            for contender, measures in experiment_results.items():
                self.results[experiment.name][contender.id()] = measures

        with open(self.filename, 'w') as out:
            stream = '{\n'
            for (experiment, contender) in sorted(self.results.items()):
                stream += '    "%s": {\n' % experiment
                for (description, results) in contender.items():
                    stream += '        %s: %s,\n' % (str(description), str(results))

                if len(contender.items()) > 0:
                    stream = stream[:-2]

                stream += '\n    },\n'

            stream += '}'
            #stream = yaml.dump(self.results, default_flow_style=False)
            return out.write(stream)

    def reject_already_measured_in(self, experiments):
        missing = []
        for experiment in experiments:
            if experiment.name not in self.results:
                missing.append(experiment)

            else:
                for contender in experiment.instances():
                    if contender.id() not in self.results[experiment.name]:
                        missing.append(experiment)
                        break

        new_plan = {experiment: experiment.instances() for experiment in missing}

        return new_plan

    def stored_results_of(self, experiments):
        results = {}
        for experiment in experiments:
            if experiment.name not in self.results:
                print("Measure missing for " + experiment.name)
                continue

            stored = self.results[experiment.name]
            values = {}
            for contender in experiment.instances():
                if contender.id() in stored:
                    values[contender] = stored[contender.id()]

            results[experiment.name] = values

        return results


import sys

from tensorlog import expt
from tensorlog import declare
from tensorlog import comline
from tensorlog import learn
from tensorlog import plearn

def setExptParams():
  #usage: [targetPredicate] [epochs]
  #get the command-line options for this experiment
  pred = 'hypernym' if len(sys.argv)<=1 else sys.argv[1]
  epochs = 30 if len(sys.argv)<=2 else int(sys.argv[2])
  # use comline.parseCommandLine to set up the program, etc
  optdict,args = comline.parseCommandLine([
      '--logging', 'warn',
      '--db', 'inputs/wnet.db|inputs/wnet.cfacts',
      '--prog','inputs/wnet-learned.ppr', '--proppr',
      '--train','inputs/wnet-train.dset|inputs/wnet-train.exam',
      '--test', 'inputs/wnet-test.dset|inputs/wnet-valid.exam'])

  prog = optdict['prog']
  # the weight vector is sparse - just the constants in the unary predicate rule
  prog.setRuleWeights(prog.db.vector(declare.asMode("rule(i)")))
  targetMode = 'i_%s/io' % pred if pred!='ALL' else None
  learner = plearn.ParallelFixedRateGDLearner(
      prog,epochs=epochs,parallel=40,regularizer=learn.L2Regularizer())
  return {'prog':prog,
          'trainData':optdict['trainData'],
          'testData':optdict['testData'],
          'targetMode':targetMode,
          'savedTestPredictions':'tmp-cache/%s-test.solutions.txt' % pred,
          'savedTrainExamples':'tmp-cache/wnet-train.examples',
          'savedTestExamples':'tmp-cache/wnet-test.examples',
          'learner':learner
    }, epochs

def runMain():
  params,_ = setExptParams()
  return expt.Expt(params).run()

if __name__=="__main__":
  runMain()

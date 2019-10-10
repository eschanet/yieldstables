import unittest
import itertools
import os
from pprint import pprint

from yieldsTable import yieldsTable

from commonHelpers.logger import logger
logger = logger.getChild(__name__)

class TestYields(unittest.TestCase):

    def test_yds(self):
        """
        Test that computing yields works as expected
        """
        selections = {}
        selections['test'] = "nJet30>=2 && mt>=400. && met>240. && meffInc30 > 600. &&  nLep_base==1&&nLep_signal==1 && ( (AnalysisType==1 && lep1Pt>7.) || (AnalysisType==2 && lep1Pt>6.))"
        config = {
            "processes" : [
                ["test", "background", [("test/references/testfile.root", "test")]],
            ],
            "selections" : selections,
            "lumifactor" : 139000,
            "weights" : "genWeight*eventWeight*pileupWeight*leptonWeight*bTagWeight*jvtWeight",
            "output_path" : "./",
            "output_name" : "yields",
        }
        yieldstable = yieldsTable(**config)
        table = yieldstable.createYieldstable()
        raw = table['test']['test']['raw']

        self.assertEqual(raw,1494)



if __name__ == "__main__":

    unittest.main()

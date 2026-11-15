import importlib.util
import json
import pathlib
import tempfile
import shutil
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]

def load_script(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
 mod=importlib.util.module_from_spec(spec)
 spec.loader.exec_module(mod)
 return mod

class AtlasTests(unittest.TestCase):
 def test_target_identifiers(self):
  t=json.loads((ROOT/'data/targets.json').read_text())['targets']
  genes=[x['gene'] for x in t]
  self.assertEqual(31,len(genes));self.assertEqual(len(genes),len(set(genes)))
  self.assertTrue({'TMEM143','LETM2','SLC25A43','SLC35F1'}.issubset(genes))
 def test_first_seen_preserved(self):
  mod=load_script('update_literature')
  p=mod.parse_item({'source':'MED','id':'123','title':'Important paper','pubYear':'2026','pmid':'123'},'LETM2',{'first_seen':'2026-11-02'},'2026-11-15')
  self.assertEqual('2026-11-02',p['first_seen'])
  self.assertEqual('https://pubmed.ncbi.nlm.nih.gov/123/',p['url'])
 def test_mock_literature_refresh_does_not_reclassify_targets(self):
  mod=load_script('update_literature')
  with tempfile.TemporaryDirectory() as td:
   tmp=pathlib.Path(td);(tmp/'data').mkdir()
   shutil.copyfile(ROOT/'data/targets.json',tmp/'data/targets.json')
   shutil.copyfile(ROOT/'data/literature.json',tmp/'data/literature.json')
   orig=mod.ROOT; mod.ROOT=tmp
   def fetch(g):
    return ([{'source':'MED','id':'777','title':f'{g} function study','pubYear':'2026','pmid':'777'}],1)
   try:
    before=(tmp/'data/targets.json').read_text()
    result=mod.update(fetch=fetch,now='2026-11-15T19:00:00+00:00',sleep=0)
    self.assertEqual(31,len(result['papers']))
    self.assertEqual(before,(tmp/'data/targets.json').read_text())
    self.assertEqual('2026-11-15',result['papers'][0]['first_seen'])
   finally:mod.ROOT=orig
 def test_site_compiles_and_contains_all_targets(self):
  mod=load_script('build_site');mod.build()
  s=(ROOT/'docs/index.html').read_text()
  self.assertIn('LETM2',s)
  self.assertIn('TMEM143',s)
  self.assertIn('Evidence watch',s)
  self.assertNotIn('__TARGETS_JSON__',s)

if __name__=='__main__':unittest.main()

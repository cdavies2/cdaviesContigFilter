# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from cdaviesContigFilter.cdaviesContigFilterImpl import cdaviesContigFilter
from cdaviesContigFilter.cdaviesContigFilterServer import MethodContext
from cdaviesContigFilter.authclient import KBaseAuth as _KBaseAuth

from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.WorkspaceClient import Workspace


class cdaviesContigFilterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('cdaviesContigFilter'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'cdaviesContigFilter',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = cdaviesContigFilter(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa
        cls.prepareTestData()

    @classmethod
    def prepareTestData(cls):
        """This function creates an assembly object for testing"""
        fasta_content = '>seq1 something soemthing asdf\n' \
                        'agcttttcat\n' \
                        '>seq2\n' \
                        'agctt\n' \
                        '>seq3\n' \
                        'agcttttcatgg'

        filename = os.path.join(cls.scratch, 'test1.fasta')
        with open(filename, 'w') as f:
            f.write(fasta_content)
        assemblyUtil = AssemblyUtil(cls.callback_url)
        cls.assembly_ref = assemblyUtil.save_assembly_from_fasta({
            'file': {'path': filename},
            'workspace_name': cls.wsName,
            'assembly_name': 'TestAssembly'
        })

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_run_cdaviesContigFilter_ok(self):
        # call your implementation
        print('test_run_cdaviesContigFilter_ok')
        ret = self.serviceImpl.run_cdaviesContigFilter(self.ctx,
                                                {'workspace_name': self.wsName,
                                                 'assembly_input_ref': self.assembly_ref,
                                                 'min_length': 10
                                                 })
        

    
    def test_run_cdaviesContigFilter_min_len_negative(self):
        print('test_run_cdaviesContigFilter_min_len_negative')
        with self.assertRaisesRegex(ValueError, 'min_length parameter cannot be negative'):
            self.serviceImpl.run_cdaviesContigFilter(self.ctx,
                                              {'workspace_name': self.wsName,
                                               'assembly_input_ref': '1/fake/3',
                                               'min_length': '-10'})

    # def my_test_run_cdaviesContigFilter_min_len_parse(self):
    #     print('test_run_cdaviesContigFilter_min_len_parse')
    #     with self.assertRaisesRegex(ValueError, 'Cannot parse integer from min_length parameter'):
    #         self.serviceImpl.run_cdaviesContigFilter(self.ctx,
    #                                           {'workspace_name': self.wsName,
    #                                            'assembly_input_ref': '1/fake/3',
    #                                            'min_length': 'ten'})
    # def test_run_cdaviesContigFilter_max(self):
    #     print('test_run_cdaviesContigFilter_max')
    #     ref='79/16/1'
    #     result = self.serviceImpl.run_cdaviesContigFilter_max(self.ctx, {
    #     'workspace_name': self.wsName,
    #     'assembly_input_ref': ref,
    #     'min_length': 100,
    #     'max_length': 1000000
    # })
    #     print(result)
    
    # def test_invalid_params(self):
    #     impl=self.serviceImpl
    #     ctx=self.ctx
    #     ws=self.wsName
    #     #Missing assembly ref
    #     with self.assertRaises(KeyError):
    #         impl.run_cdaviesContigFilter_max(ctx, {'workspace_name': ws,
    #             'min_length': 100, 'max_length': 1000000})
    #     # #Missing min length
    #     # with self.assertRaises(ValueError):
    #     #     impl.run_cdaviesContigFilter_max(ctx, {'workspace_name': ws,
    #     #         'assembly_input_ref': 'x', 'max_length': 1000000})
    #     # #Min length is negative
    #     # with self.assertRaises(ValueError):
    #     #     impl.run_cdaviesContigFilter_max(ctx, {'workspace_name': ws,
    #     #         'assembly_input_ref': 'x', 'min_length': -1, 'max_length': 1000000})
    #     # #Min length is wrong type
    #     # with self.assertRaises(ValueError):
    #     #      impl.run_cdaviesContigFilter_max(ctx, {'workspace_name': ws,
    #     #          'assembly_input_ref': 'x', 'min_length': 'x', 'max_length': 1000000})
    #     # #Assembly ref is wrong type
    #     # with self.assertRaises(ValueError):
    #     #     impl.run_cdaviesContigFilter_max(ctx, {'workspace_name': ws,
    #     #         'assembly_input_ref': 1, 'min_length': 1, 'max_length': 1000000})
    #     # #Max length is negative
    #     # with self.assertRaises(ValueError):
    #     #      impl.run_cdaviesContigFilter_max(ctx, {'workspace_name': ws,
    #     #          'assembly_input_ref': 'x', 'min_length': 100, 'max_length': -1})
    #     # #Missing max length
    #     # with self.assertRaises(KeyError):
    #     #     impl.run_cdaviesContigFilter_max(ctx, {'workspace_name': ws,
    #     #         'assembly_input_ref': 'x', 'min_length': 100})
    #     # #Max length is wrong type
    #     # with self.assertRaises(ValueError):
    #     #     impl.run_cdaviesContigFilter_max(ctx, {'workspace_name': ws,
    #     #         'assembly_ref': 'x', 'min_length': 100, 'max_length': 'X'})
    
    # def test_run_cdaviesContigFilter_test_min(self):
    #     ref='79/16/1'
    #     params={
    #         'workspace_name': self.wsName,
    #         'assembly_ref': ref,
    #         'min_length': 200000,
    #         'max_length': 6000000
    #     } 
    #     result = self.serviceImpl.run_cdaviesContigFilter_max(self.ctx, params)
    #     self.assertEqual(result[0]['n_total'], 2)
    #     self.assertEqual(result[0]['n_remaining'], 1)

    # def test_run_cdaviesContigFilter_test_max(self):
    #     ref='79/16/1'
    #     params={
    #         'workspace_name': self.wsName,
    #         'assembly_ref': ref,
    #         'min_length': 100000,
    #         'max_length': 4000000
    #     }  
    #     result= self.serviceImpl.run_cdaviesContigFilter_max(self.ctx, params)
    #     self.assertEqual(result[0]['n_total'], 2)
    #     self.assertEqual(result[0]['n_remaining'], 1)
    #     self.assertTrue(len(result[0]['filtered_assembly_ref']))
    #     self.assertTrue(len(result[0]['report_name']))
    #     self.assertTrue(len(result[0]['report_ref']))

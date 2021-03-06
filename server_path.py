######server_path.py########
import time
import logging
import argsparser
from flask_restplus import *
from flask import *

import text_kg_enrichment

ns = Namespace('knowledge_graph', description='')
args = argsparser.prepare_args()

parser = ns.parser()
parser.add_argument(
	'text', 
	type=str, 
	location='json')

req_fields = {
	'text': fields.String(\
	example = u"I visited the Louvre Abu Dhabi and Zayed National Museum today.")\
	}
yan_api_req = ns.model('yan', req_fields)

'''
rsp_fields = {\
	'status':fields.String,\
	'running_time':fields.Float\
	}

yan_api_rsp = ns.model('knowledge_graph', rsp_fields)
'''

@ns.route('/knowledge_linking')
class yan_api(Resource):
	def __init__(self, *args, **kwargs):
		super(yan_api, self).__init__(*args, **kwargs)
	#@ns.marshal_with(yan_api_rsp)
	@ns.expect(yan_api_req)
	def post(self):		
		start = time.time()
		output = {}
		try:			
			args = parser.parse_args()		
			mentions = text_kg_enrichment.text_knowledge_enrichment(
				args['text'],
				)
			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			output['linked_entity'] = [{
				'mention':m['mention'],
				'entity_wikipage_id':m['entity_wikipage_id'],
				} for m in mentions]
			return output, 200
		except Exception as e:
			output['status'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output

######server_path.py########
#!/usr/bin/python

import couchdb
from couchdb.design import *

# Fields
# - 
# - bio
# - tags
# - expertise
# - category
# - hire_date
# - job_title
# - website
# - twitter

class Database(object):

    def connect(self):
        # connect to the db, creating it if it doesnt exist. 
        couch = couchdb.Server('http://localhost:5984/')
        if 'nasaprofiles' not in couch:
            self.db = couch.create('nasaprofiles')
        else:
            self.db = couch['nasaprofiles']
        return self.db

    def configure(self):
        # define/update the views

        self.connect()
        all_docs_fun = '''
        function(doc) {
          emit(doc._id, doc);
        }
        '''
        all_docs_view = ViewDefinition('main', 'all_docs', all_docs_fun )
        all_docs_view.sync(self.db)

        recently_edited_fun = '''
        function(doc) {
          if (doc.edited) {
            emit(Date.parse(doc.edited), doc._id);
          }
        }
        '''
        recently_edited_view = ViewDefinition('main', 'recently_edited', recently_edited_fun )
        recently_edited_view.sync(self.db)

        total_customized_map = '''
        function(doc) {
          if (doc.customized) {
            emit(doc._id, 1);
          }
        }
        '''
        total_customized_reduce = '''
        function(key, values, rereduce) {
          return sum(values);
        }
        '''        
        total_customized_view = ViewDefinition('main', 'total_customized', total_customized_map, 
                                              reduce_fun=total_customized_reduce )
        total_customized_view.sync(self.db)

        tags_count_map = '''
        function(doc) {
          doc.tags.forEach(function(tag) {
            emit(tag, 1);
          });
        }
        '''
        tags_count_reduce = '''
        function(key, values, rereduce) {
          return sum(values);
        }
        '''        
        tags_count_view = ViewDefinition('main', 'tags_count', tags_count_map, 
                                         reduce_fun=tags_count_reduce )
        tags_count_view.sync(self.db)

        skills_count_map = '''
        function(doc) {
          doc.skills.forEach(function(skill) {
            emit(skill, 1);
          });
        }
        '''
        skills_count_reduce = '''
        function(key, values, rereduce) {
          return sum(values);
        }
        '''        
        skills_count_view = ViewDefinition('main', 'skills_count', skills_count_map, 
                                           reduce_fun=skills_count_reduce )
        skills_count_view.sync(self.db)



if __name__ == '__main__':
    database = Database()    
    database.configure()
    

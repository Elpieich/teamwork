# -*- encoding:utf-8 -*-

from ..core import db


class Team(db.Document):
    name = db.StringField()
    members = db.ListField(db.ReferenceField('User'))
    leader = db.ReferenceField('User')
    processes = db.ListField(db.ReferenceField('Process'))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_members(self):
        return self.members

    def get_member(self, member_id):
        for member in self.members:
            if member.get_id() == member_id:
                return member

    def set_member(self, member):
        self.members.append(member)

    def delete_member(self, member):
        self.member.remove(member)

    def set_leader(self, leader):
        self.leader = leader

    def get_leader(self):
        return self.leader

    def set_process(self, process):
        self.processes.append(process)

    def get_processes(self):
        return self.processes

    def get_process(self, process_id):
        for process in self.processes:
            if process.get_id() == process_id:
                return process
        return None

    def delete_process(self, process):
        self.processes.remove(process)

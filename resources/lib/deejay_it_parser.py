#!/usr/bin/python2
import urllib2
import simplejson as json
import resources.lib.utilz as utilz


class DeejayItParser:
    def __init__(self):
        self.base_url = 'http://www.deejay.it/api/pub/v1/'
        self.podcasts_to_skip = ('30 Songs',
                                 'Colazione da Deejay',
                                 'Dance Revolution',
                                 'Deejay Is Your Deejay',
                                 'Deejay Parade',
                                 'Djs from Mars on Radio Deejay',
                                 'FantaDeejay',
                                 'FM',
                                 'Gente della notte',
                                 'Guido al Cinema',
                                 'L\'Ultimo Bicchiere',
                                 'Megajay',
                                 'One Two One Two',
                                 'Rudy Zerbi',
                                 'Say Waaad?',
                                 'Sunday Morning',
                                 'Vic e Valentina Ricci')

    def _q_and_r(
            self,
            sp_qry):
        query_url = self.base_url + sp_qry
        hres = urllib2.urlopen(query_url)
        return json.loads(hres.read().decode("utf-8"))

    def _get_speakers(
            self,
            data):
        spks = []
        # some shows do not have a spekears property
        try:
            for spkr in data['speakers']:
                spks.append(spkr['title'])
            return ', '.join(spks)
        except KeyError:
            return None

    def get_reloaded_list(
            self):
        podcasts = {}
        index = 1
        data = self._q_and_r('programs_ondemand?section=radio')

        for show in data:
            if show['title'] not in self.podcasts_to_skip:
                podcasts.update({index: {
                    'title': show['title'],
                    'description': show['description'],
                    'icon': show['images']['size_320x240'],
                    'art': show['images']['size_full'],
                    'rid': show['reloaded_id'],
                    'pid': show['podcast_id'],
                    'speakers': self._get_speakers(show)}})
                index += 1
        return podcasts

    def get_latest_ep(
            self,
            pid,
            rid):
        query = 'archive_ondemand?last_day=1&pid=%s&rid=%s' % (pid, rid)
        data = self._q_and_r(query)
        first_json_key = data[0].keys()[0]
        ep_data = data[0][first_json_key]['reloaded']
        episode = {1: {'title': ep_data['title'],
                       'file': ep_data['file']}}
        return episode

    def get_latest_ep_date(
            self,
            pid,
            rid):
        query = 'archive_ondemand?last_day=1&pid=%s&rid=%s' % (pid, rid)
        data = self._q_and_r(query)
        return data[0].keys()[0]

    def get_episodes(
            self,
            pid,
            rid,
            ep_type,
            yyyymm=None):
        if yyyymm is None:
            date = self.get_latest_ep_date(pid, rid)
            end_date = '%s-%s-%s' % (date[0:4], date[4:6], date[6:8])
            start_date = '%s-%s-01' % (date[0:4], date[4:6])
        else:
            end_date, start_date = utilz.get_dates(yyyymm)

        eps = {}
        index = 1
        query = 'archive_ondemand?date_end=%s&date_start=%s&pid=%s&rid=%s' % (end_date, start_date, pid, rid)
        data = self._q_and_r(query)
        for d in data:
            for date in d.keys():
                for r_type in d[date].keys():
                    if r_type == ep_type:
                        eps.update({index: {
                            'title': d[date][r_type]['title'],
                            'file': d[date][r_type]['file'],
                            'date': date}})
                        index += 1
        return eps, date[0:6]

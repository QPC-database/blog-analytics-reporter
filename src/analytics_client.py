from datetime import datetime

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from config import config

KEY_FILE_LOCATION = config['KEY_FILE_LOCATION']
VIEW_ID = config['VIEW_ID']
START_DATE = config['START_DATE']

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']


def get_date():
    return datetime.today().strftime('%Y-%m-%d')


def initialize_analytics_reporting():
    credentials = Credentials.from_service_account_file(
        KEY_FILE_LOCATION, scopes=SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics


def get_page_report(analytics, title):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': START_DATE, 'endDate': get_date()}],
                    'dimensions': [{'name': 'ga:pageTitle'}],
                    'metrics': [
                        {'expression': 'ga:pageviews'},
                    ],
                    "filtersExpression": 'ga:pageTitle==' + title,
                }]
        }
    ).execute()


def get_total_report(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': START_DATE, 'endDate': get_date()}],
                    'metrics': [
                        {'expression': 'ga:pageviews'},
                        {'expression': 'ga:users'},
                    ],
                }]
        }
    ).execute()


def parse_report(response):
    page_list = []
    for report in response.get('reports', []):
        column_header = report.get('columnHeader', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get(
            'metricHeader', {}).get('metricHeaderEntries', [])
        for row in report.get('data', {}).get('rows', []):
            page = {}
            dimensions = row.get('dimensions', [])
            date_range_values = row.get('metrics', [])
            for header, dimension in zip(dimension_headers, dimensions):
                page[header] = dimension
            for i, values in enumerate(date_range_values):
                for metricHeader, value in zip(metric_headers, values.get('values')):
                    page[metricHeader.get('name')] = value
            page_list.append(page)
    list.sort(page_list, key=lambda p: int(p['ga:pageviews']), reverse=True)
    return page_list


def get_page_info(title):
    analytics = initialize_analytics_reporting()
    report = get_page_report(analytics, title=title)
    page = parse_report(report)
    if page:
        return page[0]
    else:
        return {}


def get_total_info():
    analytics = initialize_analytics_reporting()
    report = get_total_report(analytics)
    total = parse_report(report)
    return total[0]


if __name__ == '__main__':
    print(get_total_info())
    print(get_page_info('xuewenG'))

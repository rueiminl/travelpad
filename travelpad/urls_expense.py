from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^expense$', 'travelpad.views_expense.expense', name = 'expense'),
    
    #below are restful APIs
    url(r'^costs$', 'travelpad.views_expense.costs', name='cost-list'),
    url(r'^costs/(?P<cost_id>\d+)$', 'travelpad.views_expense.costs_id', name = 'cost-id'),
    url(r'^costs-user$', 'travelpad.views_expense.costs_user', name = 'cost-user'),

)


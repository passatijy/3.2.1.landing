from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    request_arg = request.GET.get('from-landing')
    print('Stats: ', request_arg)
    counter_click[request_arg]+=1
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    request_arg = request.GET.get('ab-test-arg')
    print(request_arg)
    if request_arg == 'original':
        counter_show['original'] += 1
        print(counter_show['original'])
        return render_to_response('landing.html')
    else:
        counter_show['test'] += 1
        print(counter_show['test'])
        return render_to_response('landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    if counter_click['test'] == 0 :
        test_conversion = 0
    else:
        test_conversion = counter_show['test']/counter_click['test']
    if counter_click['original'] ==0:
        orig_conversion = 0.00001
    else:
        orig_conversion = counter_show['original']/counter_click['original']
    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'test_show':counter_show['test'],
        'test_click':counter_click['test'],
        'original_conversion':orig_conversion,
        'orig_show':counter_show['original'],
        'orig_click':counter_click['original'],
    })

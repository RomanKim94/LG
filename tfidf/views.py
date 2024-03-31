from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from tfidf.forms import FileForm
from tfidf.models import TextFile
from tfidf.services import FileService


def upload(request):
    error = ''
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        formats = ('.txt', )
        # Проверяем файл на соответствие необходимому расширению
        if form.is_valid() and form.cleaned_data['file'].name.endswith(formats):
            file = TextFile(file=form.cleaned_data['file'])
            # Сохраняем файл
            file.save()
            # Направляем id загруженного файла в функцию info
            new_item_pk = TextFile.objects.last().id
            return redirect('info', pk=new_item_pk)
        else:
            error = 'Тип файла не поддерживается. Добавьте файл с расширением .txt'
    form = FileForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'tfidf/upload.html', data)


def info(request, pk):
    """
    Функция представления для отображения информации о словах загруженного файла.
    С пагинацией
    """
    try:
        data = FileService.get_td_and_idf(TextFile.objects.get(pk=pk).file.path)
        paginator = Paginator(data['info'], 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'tfidf/file_info.html', {'info': page_obj})
    except:
        return render(request, 'tfidf/error.html')
    # Закомментированный код для функции представления без пагинации
    # try:
    #     data = FileService.get_td_and_idf(TextFile.objects.get(pk=pk).file.path)
    #     return render(request, 'tfidf/file_info.html', data)
    # except:
    #     return render(request, 'tfidf/error.html')


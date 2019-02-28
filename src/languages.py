localisation = {
	#MESSAGES
	'HELLO' : 'Я бот-помощник.\nЧто я могу для вас сделать ?\n\n',
	'SENDINGPDF' : 'Высылаю PDF-файл с программой конференции',
	'WHICHDAY' : 'Какой день вас интересует ?\n\n',
	'CHOOSESECTION' : 'Выберите секцию: \n\n',
	#BUTTONS
	'SHOWPROGRAM' : 'Показать программу по дням',
	'SENDPROGRAM' : 'Прислать программу в PDF',
	'LANGUAGE' : 'English',
	'TOBEGINNING' : 'В начало',
	'BACK' : 'Назад',
	'24' : '24 сентября',
	'25' : '25 сентября',
	#SECTIONS
	'PLENARY' : 'Пленарная секция',
	'RESEARCH' : 'Исследовательская секция',
	'YOUNG' : 'Конференция молодых учёных',
	'WORKSHOPS' : 'Семинары, воркошопы, мастер-классы',
	'FOOD' : 'Еда',
	'GOODBYE' : 'До свидания!',
	'DETAILS': 'Подробнее: '
}
lang = 'rus'

def change_language():
	global localisation
	global lang 
	if lang == 'rus':
		lang = 'eng'
		
		localisation['HELLO'] = 'I am a helper bot.\nWhat can I do for you?\n\n'
		localisation['SENDINGPDF'] = 'Sending program as a PDF-file'
		localisation['WHICHDAY'] = 'Which date ?\n\n'
		localisation['CHOOSESECTION'] = 'Choose section: \n\n'
		
		localisation['SHOWPROGRAM'] = 'Show the conference program'
		localisation['SENDPROGRAM'] = 'Send the program as PDF'
		localisation['LANGUAGE'] = 'Русский'
		localisation['TOBEGINNING'] = 'To beginning'
		localisation['BACK'] = 'Back'
		localisation['24'] = '24 September'
		localisation['25'] = '25 September'
		
		localisation['PLENARY'] = 'Plenary session'
		localisation['RESEARCH'] = 'Research Papers Session'
		localisation['YOUNG'] = 'PhD and student showcase'
		localisation['WORKSHOPS'] = 'Workshops, seminars, master-classes'
		localisation['FOOD'] = 'Food'
		localisation['GOODBYE'] = 'Goodbye!'
		localisation['DETAILS'] = 'Details: '
		
	else:
		lang = 'rus'
		
		localisation['HELLO'] = 'Я бот-помощник.\nЧто я могу для вас сделать ?\n\n'
		localisation['SENDINGPDF'] = 'Высылаю PDF-файл с программой конференции'
		localisation['WHICHDAY'] = 'Какой день вас интересует ?\n\n'
		localisation['CHOOSESECTION'] =  'Выберите секцию: \n\n'
		
		localisation['SHOWPROGRAM'] = 'Показать программу по дням'
		localisation['SENDPROGRAM'] = 'Прислать программу в PDF'
		localisation['LANGUAGE'] = 'English'
		localisation['TOBEGINNING'] = 'В начало'
		localisation['BACK'] = 'Назад'
		localisation['24'] = '24 сентября'
		localisation['25'] = '25 сентября'
		
		localisation['PLENARY'] = 'Пленарная секция'
		localisation['RESEARCH'] = 'Исследовательская секция'
		localisation['YOUNG'] = 'Конференция молодых учёных'
		localisation['WORKSHOPS'] = 'Семинары, воркошопы, мастер-классы'
		localisation['FOOD'] = 'Еда'
		localisation['GOODBYE'] = 'До свидания!'
		localisation['DETAILS'] = 'Подробнее '
		


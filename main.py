import streamlit as st
import os
import json
import requests
import datetime
import calendar
import pandas as pd
import openai



from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_chat import message


page_config = {"page_title":"Dreamers Lab", "page_icon":":desktop_computer:", "layout":"centered"}
st.set_page_config(**page_config)

def load_lottiefile(filepath: str):
	with open(filepath, 'r') as file:
		return json.load(file)

def load_lottieurl(url: str):
	r = requests.get(url)
	if r.status_code != 200:
		return None
	else:
		return r.json()

fin_lottie = load_lottiefile('animation/fin1.json')
fin2_lottie = load_lottiefile('animation/fin2.json')
fin3_lottie = load_lottiefile('animation/fin3.json')

# finance_lottie = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_uf2ng6jq.json")
with st.sidebar:
	selected = option_menu(
		menu_title = 'Menu',
		options = ['Home', 'Chatbot', 'Finance', 'Health'],
		icons = ['speedometer', 'chat-dots', 'currency-bitcoin', 'activity'],
		menu_icon = 'cast',
		default_index = 0
		)


# ------------------------------------------------- Home section ----------------------------------------------------------#
if selected == 'Home':
	st.write('''

		# DreamersTech Solutions 
		


		''')


# ------------------------------------------------- End Home section ----------------------------------------------------------#




# ------------------------------------------------- Chatbot section ----------------------------------------------------------#

if selected == 'Chatbot':

	st.write('''
		# :hand: Chatbot Assistant

		''')
	openai.api_key = st.secrets["api_secret"]

	def generate_response(prompt):
		response = openai.Completion.create(
		  model="text-davinci-003",
		  prompt=prompt,
		  temperature=0,
		  max_tokens=1024,
		  top_p=1,
		  frequency_penalty=0,
		  presence_penalty=0,
		  stop=None
		)

		message = response.choices[0].text
		return message

	if 'generated' not in st.session_state:
		st.session_state['generated'] = []

	if 'past' not in st.session_state:
	    st.session_state['past'] = []

	def get_text():
		input_text = st.text_input('say something...')
		return input_text

	user_input = get_text()

	if user_input:
		output = generate_response(user_input)
		st.session_state.past.append(user_input)
		st.session_state.generated.append(output)

	if st.session_state['generated']:
		for i in range(len(st.session_state['generated'])-1, -1, -1):
			message(st.session_state["generated"][i], key=str(i))
			message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


# ------------------------------------------------- End Chatbot section ----------------------------------------------------------#





# ------------------------------------------------- Finance section ----------------------------------------------------------#


if selected == 'Finance':
	st.write('''
		# Finance
		Finance is the study and discipline of [money](https://en.wikipedia.org/wiki/Money), [currency](https://en.wikipedia.org/wiki/Currency) and [capital assets](https://en.wikipedia.org/wiki/Capital_asset). 
		It is related to, but not synonymous with [economics](https://en.wikipedia.org/wiki/Economics), which is the study of production, distribution, and consumption of money, assets, goods and services (the discipline of financial economics bridges the two). 
		Finance activities take place in financial systems at various scopes, thus the field can be roughly divided into [personal, corporate, and public finance].

		''')
	col1, col2 = st.columns(2)
	with col1:
		st_lottie(fin_lottie,
			speed=1,
			reverse=False,
			loop=True,
			quality="high",
			width=300,
			height=250,
			)
		st.write('''

			### Areas of Finance
			- **Personal Finance** -
			the mindful planning of monetary spending and saving, while also considering the possibility of future risk". Personal finance may involve paying for education, 
			financing durable goods such as real estate and cars, buying insurance, investing, and saving for retirement.

			- **Corporate Finance** -
			deals with the actions that managers take to increase the value of the firm to the shareholders, the sources of funding and the capital structure of corporations, 
			and the tools and analysis used to allocate financial resources.

			- **Public Finance** -
			describes finance as related to sovereign states, sub-national entities, and related public entities or agencies. It generally encompasses a long-term strategic 
			perspective regarding investment decisions that affect public entities.

			- **Quantitative Finance** -
			also referred to as "mathematical finance" – includes those finance activities where a sophisticated mathematical model is required.
			[read more](https://corporatefinanceinstitute.com/resources/data-science/quantitative-finance/#:~:text=Quantitative%20finance%20is%20the%20use,relates%20to%20portfolio%20management%20applications.)
			
			''')
	with col2:
		st.write('''

			### Financial system

			As above, the financial system consists of the flows of capital that take place between individuals and households [(personal finance)](https://en.wikipedia.org/wiki/Personal_finance), 
			governments [(public finance)](https://en.wikipedia.org/wiki/Public_finance), and businesses [(corporate finance)](https://en.wikipedia.org/wiki/Corporate_finance). "Finance" thus studies the process of channeling money from savers and 
			investors to entities that need it. [b] Savers and investors have money available which could earn interest or dividends if put to productive use. 
			Individuals, companies and governments must obtain money from some external source, such as loans or credit, when they lack sufficient funds to operate.
			
			''')
		st_lottie(fin2_lottie,
			speed=1,
			reverse=False,
			loop=True,
			quality="high",
			width=300,
			height=250,
			)
		st_lottie(fin3_lottie,
			speed=1,
			reverse=False,
			loop=True,
			quality="high",
			width=300,
			height=250,
			)
	st.write('''
			### Loan Calculator
			This is app is going to determine how long it takes to repay a loan borrowed, given amount borrowed, interest rates and payment terms 
		''')
	
	
	with st.form(key='form1'):
		col1, col2, col3 = st.columns(3)
		with col1:
			loan_amount = st.number_input('amount borrowed', value=0, min_value=0, max_value=int(10e10))

		with col2:
			payment_rate = st.slider('Interest rate', 0, 10)/100

		with col3:
			monthly_amount = st.number_input('Monthly re-payment', min_value=0, max_value=int(10e10))

		# submit_label = f'<i class="fas fa-calculator"></i> Calculate'

		submit = st.form_submit_button(label='Calculate')

		#Determine the total period it takes to repay off a loan
		# bal = 5000
		# interestRate = 0.13
		# monthlyPayment = 500

	if submit not in st.session_state:
		df = pd.DataFrame(columns=['End Month', 'Loan Amount', 'Interest Charge'])
		
		current_date = datetime.today()
		# print(current_date)

		end_month_day = calendar.monthrange(current_date.year, current_date.month)[1]
		days_left = end_month_day - current_date.day

		next_month_start_date = current_date + timedelta(days=days_left + 1)
		end_month = next_month_start_date

		period_count = 0
		total_int = 0
		data = []

		while loan_amount > 0:
		    int_charge = (payment_rate / 12) * loan_amount
		    loan_amount += int_charge
		    loan_amount -= monthly_amount

		    if loan_amount <= 0:
		        loan_amount = 0
		    total_int += int_charge
		    print(end_month, round(loan_amount, 2), round(int_charge, 2))

		    period_count += 1
		    new_date = calendar.monthrange(end_month.year, end_month.month)[1]
		    end_month += timedelta(days=new_date)

		    # df = df.append({'End Month': end_month, 'Loan Amount': round(loan_amount, 2), 'Interest Charge': round(int_charge, 2)}, ignore_index=True)

		    data.append([end_month.date(), round(loan_amount, 2), round(int_charge, 2)])

		    if loan_amount == 0:
		        break
		print('Total Interest Rate paid: ', total_int)
		df = pd.DataFrame(data, columns=['next_pay_date', 'amount_remaining', 'interest_amount'])

		
		years = int(period_count // 12)
		months_remaining = round(period_count % 12)
		print(f"{years} years and {months_remaining} months")

		col1, col2 = st.columns(2)
		with col1:
			st.dataframe(df, use_container_width=True)

		with col2:
			st.write('Loan payment due')
			col1, col2, col3 = st.columns(3)
			col1.metric("", str(years), " yrs")
			col2.metric("", str(months_remaining), " months")
			st.metric("Total Interest Paid", "sh. " + str(round(total_int)), "")
			# col2.metric("Wind", "9 mph", "-8%")
			# col3.metric("Humidity", "86%", "4%")



# --------------------------------------End Finance Section ----------------------------------------------------- #
		

import streamlit as st

import google.generativeai as palm
# Set your own Palm API Key
palm.configure(api_key="ADD YOUR API KEY HERE")

st.set_page_config(layout="wide")

def inputs():
    # Here we are defining the sidebar with :
    # 1) a basic input text and 2) a button 
    # We will receive the Course Name as Prompt and we are goint to call Palm API to generate the new content

    st.sidebar.header("Marketing Content Generator")

    prompt_input = st.sidebar.text_input("Prompt", placeholder =   "Write the name of the course you want to promote", )
    button = st.sidebar.button("Get Palm API response")

    return prompt_input, button



def get_generative_data(prompt_input):
    # Code from Maker Suite
    # We are receiving the Prompt from the input configured on the sidebar.
    
    defaults = {
        'model': 'models/text-bison-001',
        'temperature': 0.7,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
        'max_output_tokens': 1024,
        'stop_sequences': [],
        'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
        }

    prompt = f"""We are an online academy that generates online courses, create formal marketing content
    input: Basic Python for Teenagers.
    O_twitter: Want to learn a new skill that will help you in your future career? Learn Python! Our Python for Teenagers course will teach you the basics of Python, so you can start coding today.
    [Course link]
    O_linkedin: Are you a teenager who wants to learn how to code? Python is a powerful programming language that can be used for a variety of tasks. Our Python for Teenagers course will teach you the basics of Python, so you can start coding today.

    Enroll today and start learning Python!
    O_banner: A relevant image or graphic, such as a computer screen with code being typed on it, or a group of teenagers working on a coding project.
    A short, catchy phrase that summarizes the course, such as "Learn Python for Teenagers" or "Coding for the Future."
    A call to action, such as "Enroll now" or "Learn more."
    The course name, instructor, and start date.
    The course logo or branding.
    input: {prompt_input}
    O_twitter:"""


    # Let's call Palm API
    response = palm.generate_text(
    **defaults,
    prompt=prompt
    )
    new_gen_content = response.result


    # Let's split the result
    splitted_res = new_gen_content.split("O_")
    twitter_content = splitted_res[0]
    linkedin_content = splitted_res[1]
    banner_guidelines = splitted_res[2]


    # We will return the 3 outputs (twitter, linkedIn, and the content for the banner)
    return twitter_content, linkedin_content, banner_guidelines


def main():
    # We call the sidebar
    prompt_input, button = inputs()

    if button:
        # When the button is clicked, then we are going to show the prompt
        st.header('Content Generated for Course: "'+prompt_input+'"', divider='rainbow')

        # We call the function to get the content from Palm API and Maker Suite
        # We will receive the 3 outputs :twitter, linkedIn, and the content for the banner
        palm_res1, palm_res2, palm_res3 = get_generative_data(prompt_input)


        # Now we just need to display the results :)

        # Show the Tweet
        st.header('Twitter', divider='rainbow')
        with st.container():
            st.text(palm_res1)

        spaces, buttonCol = st.columns([4,1])
        with buttonCol:
            st.button( "Share on :blue[Twitter]", use_container_width=True)
        
        
        # Show the LinkedIn Post content
        st.header('LinkedIn Content', divider='rainbow')
        with st.container():
            st.text(palm_res2)
        
        spaces, buttonCol = st.columns([4,1])
        with buttonCol:
            st.button( "Share on :pink[Linkedin]", use_container_width=True)

        # Show the banner instruction 
        st.header('Banner Guides', divider='rainbow')
        with st.container():
            st.text(palm_res3)

        
        
        st.header('Created with :blue[_Streamlit_] :sunglasses:')



if __name__ == "__main__":
    main()

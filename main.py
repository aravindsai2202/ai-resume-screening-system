import streamlit as st
import PyPDF2
import re
from io import StringIO

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🤖",
    layout="wide"
)



# ---------------- CSS ----------------

st.markdown(
"""
<style>

body{
background:#0f172a;
}


.stApp{
background:
linear-gradient(
135deg,
#020617,
#0f172a
);
color:white;
}


.hero{

text-align:center;
padding:40px;

}


.hero h1{

font-size:55px;
font-weight:900;
background:
linear-gradient(
90deg,
#38bdf8,
#818cf8
);

-webkit-background-clip:text;
color:transparent;

}


.hero p{

font-size:22px;
color:#cbd5e1;

}



.card{

background:#111827;
padding:25px;
border-radius:20px;
border:1px solid #1e293b;
box-shadow:
0px 10px 30px rgba(0,0,0,.3);

}



.metric-card{

background:#1e293b;
padding:20px;
border-radius:18px;
text-align:center;

}


.skill{

display:inline-block;
background:#2563eb;
padding:8px 15px;
border-radius:20px;
margin:5px;
font-size:14px;

}



.good{

color:#22c55e;
font-size:22px;
font-weight:bold;

}



.bad{

color:#ef4444;
font-size:22px;
font-weight:bold;

}


.stButton button{

width:100%;
height:50px;
border-radius:15px;

background:
linear-gradient(
90deg,
#2563eb,
#7c3aed
);

color:white;
font-size:18px;
font-weight:bold;

}


</style>
""",
unsafe_allow_html=True
)



# ---------------- HEADER ----------------


st.markdown(
"""
<div class="hero">

<h1>
🤖 AI Resume Screening System
</h1>

<p>
AI Powered ATS Analysis • Resume Matching • Skill Gap Detection
</p>

</div>

""",
unsafe_allow_html=True
)



# ---------------- FUNCTIONS ----------------


def extract_pdf(file):

    text=""

    reader=PyPDF2.PdfReader(file)

    for page in reader.pages:

        text += page.extract_text() or ""

    return text



def clean(text):

    text=text.lower()

    text=re.sub(
        "[^a-z0-9 ]",
        " ",
        text
    )

    return text



def skills(text):

    skill_database=[

        "python",
        "sql",
        "mysql",
        "machine learning",
        "deep learning",
        "tensorflow",
        "keras",
        "pandas",
        "numpy",
        "scikit-learn",
        "streamlit",
        "aws",
        "aws bedrock",
        "langchain",
        "llm",
        "generative ai",
        "nlp",
        "computer vision",
        "opencv",
        "power bi",
        "excel",
        "docker"

    ]


    found=[]

    text=text.lower()


    for s in skill_database:

        if s in text:

            found.append(s)


    return found



# ---------------- SIDEBAR ----------------


with st.sidebar:


    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        width=120
    )


    st.title(
        "ATS Analyzer"
    )


    st.write(
        """
        Upload resume and job description.
        
        The system analyzes:
        
        ✔ Similarity Score
        
        ✔ Skills
        
        ✔ Missing Requirements
        
        ✔ Candidate Fit
        
        """
    )



# ---------------- INPUT AREA ----------------



col1,col2=st.columns(2)



with col1:


    st.markdown(
        "<div class='card'>",
        unsafe_allow_html=True
    )


    resume_file=st.file_uploader(
        "📄 Upload Resume PDF",
        type=["pdf"],
        key="resume_upload"
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )



with col2:


    st.markdown(
        "<div class='card'>",
        unsafe_allow_html=True
    )


    jd=st.text_area(
        "📌 Job Description",
        height=250
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )




st.write("")



analyze=st.button(
    "🚀 Analyze Resume"
)



# ---------------- PROCESS ----------------


if analyze:


    if resume_file is None:

        st.error(
            "Upload resume first"
        )


    elif jd.strip()=="":


        st.error(
            "Enter job description"
        )


    else:


        with st.spinner(
            "AI is analyzing resume..."
        ):


            resume_text=extract_pdf(
                resume_file
            )


            r=clean(
                resume_text
            )


            j=clean(
                jd
            )


            vectorizer=TfidfVectorizer(
                stop_words="english"
            )


            vectors=vectorizer.fit_transform(
                [
                    r,
                    j
                ]
            )


            score=cosine_similarity(
                vectors[0:1],
                vectors[1:2]
            )[0][0]*100



            resume_skills=skills(
                resume_text
            )


            jd_skills=skills(
                jd
            )


            matched=list(
                set(resume_skills)
                &
                set(jd_skills)
            )


            missing=list(
                set(jd_skills)
                -
                set(resume_skills)
            )



        # -------- DASHBOARD --------


        st.divider()


        st.subheader(
            "📊 ATS Performance Dashboard"
        )


        c1,c2,c3=st.columns(3)



        with c1:

            st.metric(
                "ATS Score",
                f"{score:.1f}%"
            )


        with c2:

            st.metric(
                "Matched Skills",
                len(matched)
            )


        with c3:

            st.metric(
                "Missing Skills",
                len(missing)
            )



        st.divider()



        st.subheader(
            "✅ Matched Skills"
        )


        if matched:

            for x in matched:

                st.markdown(
                    f"<span class='skill'>{x}</span>",
                    unsafe_allow_html=True
                )

        else:

            st.write(
                "No matched skills"
            )



        st.subheader(
            "❌ Missing Skills"
        )


        if missing:

            for x in missing:

                st.markdown(
                    f"<span class='skill'>{x}</span>",
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "No missing skills 🎉"
            )



        st.subheader(
            "🤖 AI Recommendation"
        )


        if score>=70:

            st.success(
                "Strong candidate. Resume matches job requirements well."
            )

        elif score>=40:

            st.warning(
                "Moderate match. Improve missing skills."
            )

        else:

            st.error(
                "Low match. Customize resume for this role."
            )



        st.subheader(
            "📄 Resume Content"
        )


        with st.expander(
            "View Extracted Resume"
        ):

            st.text(
                resume_text
            )



        report=f"""
AI Resume Screening Report

ATS Score:
{score:.2f}%

Matched Skills:
{matched}

Missing Skills:
{missing}

Recommendation:
Resume analysis completed.
"""


        st.download_button(

            "⬇ Download Report",

            report,

            file_name="ATS_Report.txt"

        )



st.divider()


st.caption(
"Built using Python | Streamlit | NLP | Machine Learning"
)
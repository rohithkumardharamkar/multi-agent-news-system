from textwrap import dedent


def build_planner_prompt(query: str) -> str:
    return dedent(
        f"""
        You are a News Planning Agent.

        User Query:
        {query}

        Latest News Context:

        Determine which news categories are relevant.

        Available Categories:
        - International
        - National
        - Sports
        - Business

        Rules:
        1. Return ONLY a JSON array.
        2. Do not return explanations.
        3. Use exact category names.

        Examples:

        ["Sports"]

        ["Business","International"]

        ["National","Business"]

        JSON:
        """
    ).strip()


def build_relevance_prompt(
    query: str,
    is_exam_prep: bool,
    article_list: list[str],
) -> str:
    articles = "\n".join(article_list)
    return dedent(
        f"""
        You are a News Ranking Agent.

        User Query:
        {query}

        UPSC Mode:
        {is_exam_prep}

        Articles:
        {articles}

        Task:
        1. Score each article for:
           - Query Relevance (1-10)
           - Educational Value (1-10)

        2. Select the best 5 articles.

        3. Return ONLY the URLs.

        Example:

        https://example1.com
        https://example2.com
        https://example3.com

        No explanations.
        """
    ).strip()


def build_factcheck_prompt(news: str) -> str:
    return dedent(
        f"""
        Fact Check the following news summary:
        {news[:3000]}
        Identify any potential misinformation or unverified claims.
        Provide a credibility score (0-10) and a brief justification for each major point.
        Return the verified/cleaned version of the news.
        """
    ).strip()


def build_summary_prompt(news: str, is_exam_prep: bool) -> str:
    if is_exam_prep:
        summary_instructions = dedent(
            """
            Format this as an EXAM-PREP DIGEST. For each major point:
            1. Context/Background.
            2. Key Facts/Stats.
            3. Significance for Exam/Policy Impact.

            Keep it highly informative and data-rich. Avoid fluff.
            """
        ).strip()
    else:
        summary_instructions = (
            "Maintain a professional tone and highlight key takeaways."
        )

    return dedent(
        f"""
        Summarize the following verified news into a concise digest:
        {news[:4000]}

        {summary_instructions}
        """
    ).strip()


def build_reflection_prompt(summary: str) -> str:
    return dedent(
        f"""
        You are a Quality Review Agent.

        NEWS SUMMARY:
        {summary}

        TASK:
        Review the summary for:

        - Clarity
        - Structure
        - Readability
        - Redundancy
        - Grammar

        RULES:
        - Do NOT introduce new facts.
        - Do NOT suggest missing facts.
        - Do NOT use outside knowledge.
        - Evaluate only the provided summary.

        OUTPUT:

        Strengths:
        - ...

        Weaknesses:
        - ...

        Writing Improvements:
        - ...
        """
    ).strip()

def build_critic_prompt(summary: str, reflection: str) -> str:
    return dedent(
        f"""
        Review the news summary and its reflection:
        Summary: {summary}
        Reflection: {reflection}
        Act as a sharp editor for a UPSC news magazine.
        Point out any bias, verbosity, or missing key facts.
        Provide constructive criticism to improve academic rigor.
        """
    ).strip()


def build_magazine_prompt(summary: str,critique: str,is_exam_prep: bool,) -> str:
    if is_exam_prep:
        tone_and_style = dedent(
            """
            Use an ANALYTICAL and INFORMATIVE tone.
            Instead of a 'vibrant' style, use a 'Bureaucratic/Academic' style.
            Ensure sub-headlines correlate to UPSC GS categories (e.g., GS-II: Governance, GS-III: Economy).
            Include a 'Quick Facts for Prelims' section.
            """
        ).strip()
    else:
        tone_and_style = "Use a vibrant and engaging tone."

    return dedent(
        f"""
        Create a professional magazine-style report based on the news summary and the editor's critique.
        Summary: {summary}
        Critique: {critique}
        The final report should include:
        1. A catchy headline.
        2. Sectioned content with sub-headlines.
        3. Key takeaways.
        4. A professional conclusion.
        5. A 'Direct Source Links' section at the end for further reading.
        {tone_and_style}
        """
    ).strip()

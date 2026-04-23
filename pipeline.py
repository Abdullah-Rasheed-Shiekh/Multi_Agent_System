from agents import reader_agent, search_agent, writer_chain, critic_chain

def research_pipeline(topic:str) -> dict:
    state={}

    print("\n"+" ="*30)
    print("Step 1 - Searching ... ")
    print("\n"+" ="*30)

    search_agent_working = search_agent()
    search_result=search_agent_working.invoke({
        "messages":[("user",f"Find recent, reliable and detailed information about: {topic}")]
    })

    state["search_results"] = search_result['messages'][-1].content  #Extract Last Message

    print("\n Search Result: ",state["search_results"])

    #Scrapper
    print("\n"+" ="*30)
    print("Step 2 - Scraping Reader Agent ... ")
    print("\n"+" ="*30)

    reader_agent_working = reader_agent()
    reader_result=reader_agent_working.invoke({
        "messages":[("user",
                     f"Based on the following search results about '{topic}',"
                     f"Pick the most relevant URL and scrape it for deeper content. \n\n"
                     f"Search Results: \n{state['search_results'][:800]}" 
                     )]
    })

    state['scraped_content']= reader_result['messages'][-1].content

    print("\n Scraped Result: ",state['scraped_content'])


    #Writer
    print("\n"+" ="*30)
    print("Step 3 - Writing Report Agent ... ")
    print("\n"+" ="*30)

    research_combined_agent = [
        f"SEARCH RESULTS: \n {state['search_results']} \n\n"
        f"DETAILED SEARCH RESULTS SCRAPED: \n {state['scraped_content']}"
    ]

    state["report"]=writer_chain.invoke(
        {
            "topic":topic,
            "research":research_combined_agent
        }
    )

    print("\n Final Report\n",state["report"])


    #Critic
    print("\n"+" ="*30)
    print("Step 4 - Critic is Reviewing Writing Report Agent ... ")
    print("\n"+" ="*30)

    state["feedback"]=critic_chain.invoke({
        "report": state["report"]
    })

    print("\n Critic Report\n",state["feedback"])

    return state

if __name__ == "__main__":
    topic = input("\n Enter Research Topic: ")
    research_pipeline(topic)
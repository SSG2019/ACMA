import yaml
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from Agent_enhance.tools_library.tools_math import calculate_circle_area, calculate_pairwise_distances

path = 'config/Agents.yaml'
with open(path, 'r') as file:
    agents = yaml.safe_load(file)
path = 'config/tasks.yaml'
with open(path, 'r') as file:
    tasks = yaml.safe_load(file)

class Agent_HAPS():
    def __init__(self, model):

        self.agent_config = agents
        self.task_config = tasks
        self.model = ChatOpenAI(model=model, temperature=0)

        prompt = ChatPromptTemplate.from_messages([
            ("system", f"{self.agent_config['single_haps']['role']}"),
            ("user", f"{self.task_config['single_haps']['description']}"),
        ])
        self.chain = prompt | self.model | StrOutputParser()

    def get_target(self, no_haps, analysis, airships_information, current_decision, json_template):
        quest = {"no_haps": no_haps,
                 "analysis": analysis,
                 "airships_information": airships_information,
                 "current_decision": current_decision,
                 "json_template": json_template}
        response = self.chain.invoke(quest)
        return response

class Agent_analysis():
    def __init__(self, model):

        self.agent_config = agents
        self.task_config = tasks
        self.model = ChatOpenAI(model=model, temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"{self.agent_config['auxiliary_analysis']['role']}"),
            ("user", f"{self.task_config['auxiliary_analysis']['description']}"),
        ])
        self.chain = prompt | self.model | StrOutputParser()


    def get_analysis(self, airships_information, info_history, analysis_template):
        quest = {"airships_information": airships_information,
                 "info_history": info_history,
                 "analysis_template": analysis_template}
        response = self.chain.invoke(quest)
        return response

class Agent_overlap():
    def __init__(self, model):

        self.agent_config = agents
        self.task_config = tasks
        self.tools = [calculate_pairwise_distances]
        self.model = ChatOpenAI(model=model, temperature=0).bind_tools(self.tools)
        self.messages = [SystemMessage(f"{self.agent_config['overlap_detection']['role']}")]


    def overlap_optimization_tools(self, currect_decision):
        self.messages = self.messages[:1]
        haps_positions = {}
        for date_key, haps_targets in currect_decision.items():
            # 遍历每个 HAPS 的数据
            for haps, details in haps_targets.items():
                haps_positions[haps] = tuple(details['target_position'])

        self.messages.append(HumanMessage(f"Please use the tool to calculate the distances between the four HAPS target locations. The HAPS target locations are as follows:{haps_positions}"))


        # quest = {"airships_information": airships_information,
        #          "info_history": info_history,
        #          "analysis_template": analysis_template}
        ai_msg = self.model.invoke(self.messages)
        self.messages.append(ai_msg)


        for tool_call in ai_msg.tool_calls:
            selected_tool = {"calculate_pairwise_distances": calculate_pairwise_distances}[tool_call["name"].lower()]
            tool_msg = selected_tool.invoke(tool_call)
            self.messages.append(tool_msg)

        self.messages.append(HumanMessage(f"{self.task_config['overlap_detection']['description']}".format(
            currect_decision=currect_decision)))

        response = self.model.invoke(self.messages)
        response = response.content

        return response

class Agent_event():
    def __init__(self, model):

        self.agent_config = agents
        self.task_config = tasks
        self.model = ChatOpenAI(model=model, temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"{self.agent_config['event_driven']['role']}"),
            ("user", f"{self.task_config['event_driven']['description']}"),
        ])
        self.chain = prompt | self.model | StrOutputParser()


    def get_final(self, airships_information, currect_decision, special_events, current_time):
        quest = {"airships_information": airships_information,
                 "currect_decision": currect_decision,
                 "special_events": special_events,
                 "current_time": current_time}
        response = self.chain.invoke(quest)
        return response



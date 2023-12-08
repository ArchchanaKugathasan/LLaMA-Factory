def construct_json(filename, prompt_num=1, few_show=False):
    df = read_data(filename)
    json_list = []
    if few_show:
        instruction_example = instruction_example = " You can use the following three examples as references.\nExample 1:\nChinese source: 一路顺风，一切顺利。我爱你。小黄人\nEnglish translation: All the way, smooth sailing. I love you. Minions\nThe score in terms of emotion preservation for the translation is 0.\n\nExample 2:\nChinese source: 我一天天的赶上客服员了，谁TM得罪人了都得我收底！我教你咋干活可以！还有义务教你怎么说话怎么做人吗？\nEnglish translation: I'm catching up with the customer service staff day by day, and whoever TM offends will have to accept it! I'll teach you how to work! Do you still have the obligation to teach you how to speak and be a person?\nThe score in terms of emotion preservation for the translation is -40.\nThe parts in the source that are incorrectly translated are: The parts in the source that are incorrectly translated are: 我一天天的赶上客服员了, TM, 都得我收底, 我教你咋干活可以！还有义务教你怎么说话怎么做人吗？\nThe parts in the target that are incorrectly translated are: I'm catching up with the customer service staff day by day, TM, will have to accept it, I'll teach you how to work! Do you still have the obligation to teach you how to speak and be a person?\n\nExample 3:\nChinese source: 我现在怎么觉得，只要是女的都长的比我好看\nEnglish translation: What do I think now, as long as it's a girl, she looks better than me\nThe score in terms of emotion preservation for the translation is -1.\nThe parts in the source that are incorrectly translated are: 我现在怎么觉得.\nThe parts in the target that are incorrectly translated are: What do I think now.\n\nExample for scoring:\n Chinese source: "
    else:
        instruction_example = ""
 
    if prompt_num == 1:
        instruction_ins = "Score the following translation from Chinese to English with respect to the preservation of emotion in the source on a continuous scale from 0 to -100, where a score of minus one hundred means 'emotions are critically damaged in multiple places in the text' and score of zero means 'perfect emotion preservation'. A score of -1 means 'very subtle difference in emotion between the source and the target'. If the score is not zero (not perfect translation), please list keywords or parts of sentences in both source and target where translation is incorrect.\nChinese source: "
    elif prompt_num == 2:
        instruction_ins = "Please imagine you are a teacher of a Chinese-English translation course. Now you are assessing the translation quality of students’ course work. Please score the following translation from Chinese to English with respect to the preservation of emotion in the source on a continuous scale from 0 to -100, where a score of minus one hundred means 'emotions are severely damaged in multiple places in the text' and a score of zero means 'perfect emotion preservation'. A score of minus one means 'very subtle difference in emotion between the source and the target'. If the score is not zero (imperfect translation), please list keywords or parts of sentences in both source and target where translation is incorrect as feedback for students. Your assessment is vital to whether a student pass this course.\nChinese source: "
    elif prompt_num == 3:
        instruction_ins = "Score the following translation from Chinese to English with respect to errors in the preservation of emotion in translation. The score is calculated based on the number of errors and the level of error severity and weights assigned to each severity level, that is, minor, major and critical. One minor error in emotion preservation, leading to the slight change of emotion after translation, gets a score of -1; one major error, pertaining to the change of emotion into a different category after translation, gets a score of -5; and one critical error, resulting in the change of emotion into an extremely different or even opposite category after translation, gets a score of -10. If there is no error in terms of emotion preservation, the score is 0, which means ‘perfect emotion preservation’. We set a score of -100 as the worst score, which means ‘there are more than 10 critical errors in emotion preservation’. If the score is not 0 (imperfect translation), please list keywords or parts of sentences in both source and target where error occurs.\nChinese source: "
    else:
        raise ValueError("prompt_num should be 1, 2 or 3, but got {}".format(prompt_num))
    
    instruction_pre = instruction_ins + instruction_example
    instruction_post = "\nEnglish translation: "
 
    output_pre = "The score in terms of emotion preservation for the translation is "
    output_source = "\nThe parts in the source that are incorrectly translated are: "
    output_mt = "\nThe parts in the target that are incorrectly translated are: "
 
    for i in range(len(df)):
        json_dict = {}
        instruction = instruction_pre + df.source.values[i] + instruction_post + df.MT.values[i]
        json_dict["instruction"] = instruction
        json_dict["input"] = ""
        
        # construct output
        if df.source_keywords.values[i] != "[]":
            source_keywords = ", ".join(ast.literal_eval(df.source_keywords.values[i]))
        else:
            source_keywords = ""
        if df.mt_keywords.values[i] != "[]":
            mt_keywords = ", ".join(ast.literal_eval(df.mt_keywords.values[i]))
        else:
            mt_keywords = ""
        # omit keywords if it's empty string
        if source_keywords != "" and mt_keywords != "":
            output = output_pre + str(df.scores.values[i]) + output_source + source_keywords + output_mt + mt_keywords
        if source_keywords != "" and mt_keywords == "":
            output = output_pre + str(df.scores.values[i]) + output_source + source_keywords
        if source_keywords == "" and mt_keywords != "":
            output = output_pre + str(df.scores.values[i]) + output_mt + mt_keywords
        if source_keywords == "" and mt_keywords == "":
            output = output_pre + str(df.scores.values[i])
 
        json_dict["output"] = output
        json_list.append(json_dict)
 
    return json_list
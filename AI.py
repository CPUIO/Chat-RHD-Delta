from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def chatAI(user_input, history = None):

	ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
	
	bot_input_ids = torch.cat([history, new_user_input_ids], dim=-1) if history is not None else new_user_input_ids

	history = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

	bot_response = tokenizer.decode(history[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

	return bot_response, chat_history_ids


def main():
	history = None
	while True:
		text = input(">> ")
		bot_response, history = chat_with_bot(user_input, history)
		print("<< ", bot_response)


if __name__=="__main__":
	main()

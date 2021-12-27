import torch
from tqdm import tqdm

from sense_tune.load_data.sense_select import Sense_Selection_Data, SentDataset
from sense_tune.model.bert import forward, get_model_and_tokenizer


def get_BERT_score(data):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model, tokenizer = get_model_and_tokenizer('Maltehb/danish-bert-botxo',
                                               device,
                                               checkpoint='sense_tune/model/checkpoints/metrics_bert.pt')

    dataloader = SentDataset(Sense_Selection_Data(data, tokenizer, data_type='reduce'))

    nb_eval_steps = 0
    score = {}

    iterator = tqdm(dataloader, desc="Iteration")

    for batches in iterator:
        if len(batches) < 1:
            continue

        model.eval()
        with torch.no_grad():

            labels = batches[0][5] #if isinstance(model, BertSense) else [b[1] for b in batches]

            # run model
            for batch in batches:
                logits = forward(model, batch[2:], device)
                score[batch[1]] = logits

        nb_eval_steps += 1

    data['score'] = score

    return data

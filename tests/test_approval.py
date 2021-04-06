from openapi_elm_client.generate import generate_elm_client


def test_approval(godkjenn, corpus_spec):
    code = generate_elm_client(corpus_spec, 'Test')
    godkjenn.verify_text(code)
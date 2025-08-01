# coding=utf-8

import traceback
from typing import Dict

from django.utils.translation import gettext_lazy as _, gettext

from common.exception.app_exception import AppApiException
from common.forms import BaseForm, PasswordInputField, SingleSelect, SliderField, TooltipLabel
from models_provider.base_model_provider import BaseModelCredential, ValidCode


class AliyunBaiLianTTSModelGeneralParams(BaseForm):
    """
    Parameters class for the Aliyun BaiLian TTS (Text-to-Speech) model.
    Defines fields such as voice and speech rate.
    """

    voice = SingleSelect(
        TooltipLabel(_('Timbre'), _('Chinese sounds can support mixed scenes of Chinese and English')),
        required=True,
        default_value='longxiaochun',
        text_field='value',
        value_field='value',
        option_list=[
            {'text': _('Long Xiaochun'), 'value': 'longxiaochun'},
            {'text': _('Long Xiaoxia'), 'value': 'longxiaoxia'},
            {'text': _('Long Xiaochen'), 'value': 'longxiaocheng'},
            {'text': _('Long Xiaobai'), 'value': 'longxiaobai'},
            {'text': _('Long Laotie'), 'value': 'longlaotie'},
            {'text': _('Long Shu'), 'value': 'longshu'},
            {'text': _('Long Shuo'), 'value': 'longshuo'},
            {'text': _('Long Jing'), 'value': 'longjing'},
            {'text': _('Long Miao'), 'value': 'longmiao'},
            {'text': _('Long Yue'), 'value': 'longyue'},
            {'text': _('Long Yuan'), 'value': 'longyuan'},
            {'text': _('Long Fei'), 'value': 'longfei'},
            {'text': _('Long Jielidou'), 'value': 'longjielidou'},
            {'text': _('Long Tong'), 'value': 'longtong'},
            {'text': _('Long Xiang'), 'value': 'longxiang'},
            {'text': 'Stella', 'value': 'loongstella'},
            {'text': 'Bella', 'value': 'loongbella'},
        ]
    )

    speech_rate = SliderField(
        TooltipLabel(_('Speaking speed'), _('[0.5, 2], the default is 1, usually one decimal place is enough')),
        required=True,
        default_value=1,
        _min=0.5,
        _max=2,
        _step=0.1,
        precision=1
    )


class AliyunBaiLianTTSModelCredential(BaseForm, BaseModelCredential):
    """
    Credential class for the Aliyun BaiLian TTS (Text-to-Speech) model.
    Provides validation and encryption for the model credentials.
    """

    api_key = PasswordInputField("API Key", required=True)

    def is_valid(
        self,
        model_type: str,
        model_name: str,
        model_credential: Dict[str, object],
        model_params,
        provider,
        raise_exception: bool = False
    ) -> bool:
        """
        Validate the model credentials.

        :param model_type: Type of the model (e.g., 'TTS').
        :param model_name: Name of the model.
        :param model_credential: Dictionary containing the model credentials.
        :param model_params: Parameters for the model.
        :param provider: Model provider instance.
        :param raise_exception: Whether to raise an exception on validation failure.
        :return: Boolean indicating whether the credentials are valid.
        """
        model_type_list = provider.get_model_type_list()
        if not any(mt.get('value') == model_type for mt in model_type_list):
            raise AppApiException(
                ValidCode.valid_error.value,
                gettext('{model_type} Model type is not supported').format(model_type=model_type)
            )

        required_keys = ['api_key']
        for key in required_keys:
            if key not in model_credential:
                if raise_exception:
                    raise AppApiException(
                        ValidCode.valid_error.value,
                        gettext('{key} is required').format(key=key)
                    )
                return False

        try:
            model = provider.get_model(model_type, model_name, model_credential, **model_params)
            model.check_auth()
        except Exception as e:
            traceback.print_exc()
            if isinstance(e, AppApiException):
                raise e
            if raise_exception:
                raise AppApiException(
                    ValidCode.valid_error.value,
                    gettext(
                        'Verification failed, please check whether the parameters are correct: {error}'
                    ).format(error=str(e))
                )
            return False

        return True

    def encryption_dict(self, model: Dict[str, object]) -> Dict[str, object]:
        """
        Encrypt sensitive fields in the model dictionary.

        :param model: Dictionary containing model details.
        :return: Dictionary with encrypted sensitive fields.
        """
        return {
            **model,
            'api_key': super().encryption(model.get('api_key', ''))
        }

    def get_model_params_setting_form(self, model_name: str):
        """
        Get the parameter setting form for the specified model.

        :param model_name: Name of the model.
        :return: Parameter setting form.
        """
        return AliyunBaiLianTTSModelGeneralParams()
